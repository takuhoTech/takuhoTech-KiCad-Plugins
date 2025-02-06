import pcbnew
import os
import math
import wx
from .dialog import Dialog

class ViaFenceAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Via Fence Generator"
        self.category = "Modify PCB"
        self.description = "Add via fence to selected tracks"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./32x32.png")
        self.show_toolbar_button = True

        self.lstDefinedViaSizesOnChoiceIsCalled = False #定義済みサイズが選択されたときの自動テキスト入力により定義済みサイズの選択が解除されてしまうことを避けるためのフラグ
        self.chkUseZoneClearanceOnCheckBoxIsCalled = False

    #def __init__(self):を使うと怒られが発生する

    def CreateVia(self, brd, pos, diameter, drill, netname, isFree, viaType, startLayerID = pcbnew.F_Cu, endLayerID = pcbnew.B_Cu, removeUnconnectedAnnularRing = False):
        via = pcbnew.PCB_VIA(brd)
        via.SetPosition(pcbnew.VECTOR2I(pos[0], pos[1]))
        via.SetWidth(diameter) #外径
        via.SetDrill(drill)    #ドリル径
        via.SetNet(brd.FindNet(netname)) #ネット
        via.SetIsFree(isFree)            #True=手動でビアを置く場合と同じく自動更新されない False=ビアのネットは置かれた場所によって自動更新される
        via.SetViaType(viaType)          #pcbnew.VIATYPE_THROUGH,pcbnew.VIATYPE_BLIND_BURIED,pcbnew.VIATYPE_MICROVIA,pcbnew.VIATYPE_NOT_DEFINEDのどれか
        via.SetLayerPair(startLayerID, endLayerID) #レイヤーのID 導体レイヤーは0から31
        via.SetRemoveUnconnected(removeUnconnectedAnnularRing) #True=始点,終点,および接続されたレイヤー False=すべての導体レイヤー
        brd.Add(via)

    def AppendPosition(self, pos_list, pos): #座標リストに座標を追加する関数 リストの座標のいずれかと距離がごく近いものは追加されない 円弧と直線の接続部にビアが重なって生成されるのを防ぐが既に基板上にあるビアに対しては無力
        if any(math.dist(pos_stored, pos) < pcbnew.FromMM(0.1) for pos_stored in pos_list): #0.1mm以下の距離には複数のビアを配置しない
            return #すでに登録された座標のどれかと距離が近すぎるので新しく登録せずに終了
        pos_list.append(pos)

    def IsNum(self, s): #文字列が数値を表しているか
        try:
            float(s)
            return True
        except ValueError:
            return False
    '''
    def IsPositiveNum(self, s): #文字列が正の数値を表しているか否か
        try:
            if float(s) > 0: #正の数値
                return True
            else: #0以下の数値
                return False
        except ValueError: #そもそも数値ではない
            return False
    '''
    def IsViaSizeValid(self, txtDiameter, txtHole): #ビアサイズが有効な数値であるか
        try:
            if all([float(txtDiameter) > 0, float(txtHole) > 0, float(txtDiameter) > float(txtHole)]): #ここにアニュラリングの最小幅も含める？
                return True
            else:
                return False
        except ValueError: #そもそも数値ではない
            return False

    def OKButtonControl(self): #OKボタンを押してもよい諸条件を記述
        self.dlg.subsubSizer3OK.Enable(all([
            self.dlg.lstStartLayer.GetSelection() != self.dlg.lstEndLayer.GetSelection(), #レイヤーが同じではない
            self.IsNum(self.dlg.txtTrackToViaClearance.GetValue()), #クリアランスが数字である クリアランスは0以下でもよい
            self.IsViaSizeValid(self.dlg.txtViaDiameter.GetValue(), self.dlg.txtViaHole.GetValue()) #ビアサイズが有効な数値であるか
        ]))

    #クリアランス入力補間に関わる割り込み関数------------------------------------------------------------------------------------------------------------
    def chkUseZoneClearanceOnCheckBox(self, event):
        if self.dlg.chkUseZoneClearance.IsChecked(): #Use zone clearanceが有効になったとき,テキストボックスにゾーンのクリアランスを入力
            self.chkUseZoneClearanceOnCheckBoxIsCalled = True
            self.dlg.txtTrackToViaClearance.SetValue(str(pcbnew.ToMM(self.ZoneClearanceList[self.dlg.lstViaNet.GetSelection()])))
            self.chkUseZoneClearanceOnCheckBoxIsCalled = False

        self.OKButtonControl()

    def txtTrackToViaClearanceOnText(self, event): #上の関数内のSetValueフラグが立っていないときチェックを外す
        if not self.chkUseZoneClearanceOnCheckBoxIsCalled:
            self.dlg.chkUseZoneClearance.SetValue(False)

        self.OKButtonControl()
    #-------------------------------------------------------------------------------------------------------------------------------------------------

    #ビアサイズ入力補間に関わる割り込み関数--------------------------------------------------------------------------------------------------------------
    def lstDefinedViaSizesOnChoice(self, event): #定義済みビアサイズが選択されたとき,テキストボックスに定義済みサイズを入力
        if self.dlg.lstDefinedViaSizes.GetSelection() != wx.NOT_FOUND:
            self.lstDefinedViaSizesOnChoiceIsCalled = True
            self.dlg.txtViaDiameter.SetValue(str(pcbnew.ToMM(self.ViasDimensionsList[self.dlg.lstDefinedViaSizes.GetSelection() + 1].m_Diameter)))
            self.dlg.txtViaHole.SetValue(str(pcbnew.ToMM(self.ViasDimensionsList[self.dlg.lstDefinedViaSizes.GetSelection() + 1].m_Drill)))
            self.lstDefinedViaSizesOnChoiceIsCalled = False

        self.OKButtonControl()

    def txtViaSizesOnText(self, event): #上の関数内のSetValueフラグが立っていないとき定義済みビアサイズの選択を外す
        if not self.lstDefinedViaSizesOnChoiceIsCalled:
            self.dlg.lstDefinedViaSizes.SetSelection(wx.NOT_FOUND)

        self.OKButtonControl()
    #-------------------------------------------------------------------------------------------------------------------------------------------------

    #レイヤーペアの判定と操作の関数(レイヤーペアが隣接していれば当然アニュラリングはAll copper layersに必要になる)--------------------------------------------
    def checkViaLayerPairAdjacency(self):
        if abs(self.dlg.lstStartLayer.GetSelection() - self.dlg.lstEndLayer.GetSelection()) == 1: #レイヤーが隣接
            self.dlg.lstAnnularRings.SetSelection(0) #All copper layersにする
            self.dlg.lstAnnularRings.Enable(False)   #グレーアウトでAll copper layersに固定
        else:
            self.dlg.lstAnnularRings.Enable(True)
    #-------------------------------------------------------------------------------------------------------------------------------------------------

    #ビアタイプの判定と操作の関数(ビアタイプがthroughならばレイヤーペアはF.Cu,B.Cuでないといけない)----------------------------------------------------------
    def checkViaTypeAndSetLayerPair(self):
        if self.dlg.lstViaType.GetSelection() == 0: #throughが選択されたときレイヤー設定をF.CuとB.Cuにしてからグレーアウト
            self.dlg.lstStartLayer.SetSelection(0)  #F.Cu
            self.dlg.lstEndLayer.SetSelection(self.dlg.lstEndLayer.GetCount() - 1) #B.Cu
            self.dlg.lstStartLayer.Enable(False)    #グレーアウトでF.Cu,B.Cuに固定
            self.dlg.lstEndLayer.Enable(False)

            self.checkViaLayerPairAdjacency()       #変更されたレイヤーペアの隣接判定とそれに伴う設定

        else: #through以外でグレーアウトを解除
            self.dlg.lstStartLayer.Enable(True)
            self.dlg.lstEndLayer.Enable(True)
    #-------------------------------------------------------------------------------------------------------------------------------------------------

    def lstViaTypeOnChoice(self, event):   #ビアタイプ変更時に呼ばれる割り込み関数
        self.checkViaTypeAndSetLayerPair()

        self.OKButtonControl()

    def lstLayerPairOnChoice(self, event): #レイヤーペア変更時に呼ばれる割り込み関数
        self.checkViaLayerPairAdjacency()  #変更されたレイヤーペアの隣接判定とそれに伴う設定

        self.OKButtonControl()

    def Run(self): #ツールバーアイコンが押された時に実行
        #ダイアログと基板のオブジェクトを作成----------------------------------------------------------------------------------------------------------------
        pcb_frame = next(
            x for x in wx.GetTopLevelWindows() if x.GetName() == "PcbFrame"
        )
        self.dlg = Dialog(pcb_frame)
        board = pcbnew.GetBoard()
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #配線とビアのクリアランスの補間制御------------------------------------------------------------------------------------------------------------------
        self.dlg.chkUseZoneClearance.Bind(wx.EVT_CHECKBOX, self.chkUseZoneClearanceOnCheckBox) #Use zone clearanceの状態が変化したときに関数を呼び出す

        self.dlg.txtTrackToViaClearance.Bind(wx.EVT_TEXT, self.txtTrackToViaClearanceOnText)
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #すべてのゾーンのネットを登録しクリアランスを取得------------------------------------------------------------------------------------------
        self.ZoneClearanceList = []
        for zone in board.Zones(): #登録されないネット無しゾーンにもindexがあるからここにindexつけるのは良くない
            netname = zone.GetNetname()
            if netname != None and netname != "":  #ネット無しゾーンは登録しないしクリアランスの取得もしない
                self.dlg.lstViaNet.Append(netname) #ネット名が同じゾーンは重複せずそれぞれ登録される
                if "GND" in netname:
                    self.dlg.lstViaNet.SetSelection(self.dlg.lstViaNet.GetCount() - 1) #現在登録されている数を使うと直近で登録されたものを選べる
                self.ZoneClearanceList.append(zone.GetLocalClearance())

        self.dlg.lstViaNet.Bind(wx.EVT_CHOICE, self.chkUseZoneClearanceOnCheckBox) #ネットが変わったときにクリアランスも更新 チェックが入った時と同じ操作なので関数も同じ
        '''
        #ゾーンのものに限らずすべてのネットを登録する場合
        nets = board.GetNetsByName()
        for index, (_ , net) in enumerate(nets.items(), -1): #ダミーのネット(None?)が存在しているため実際に登録されるのはindex=0番から
            netname = net.GetNetname()
            if netname != None and netname != "":
                self.dlg.lstViaNet.Append(netname) #同名ネットがあっても表示上は一つ
                if "GND" in netname:
                    self.dlg.lstViaNet.SetSelection(index)
        '''
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #定義済みビアサイズリストの取得と登録と補間制御-------------------------------------------------------------------------------------------------------
        self.ViasDimensionsList = board.GetViasDimensionsList()
        for index, ViaDimension in enumerate(self.ViasDimensionsList): #0個目(最初)のDiameterとDrillは0になるので登録されない
            if ViaDimension.m_Diameter != 0 and ViaDimension.m_Drill != 0:
                self.dlg.lstDefinedViaSizes.Append(str(pcbnew.ToMM(ViaDimension.m_Diameter)) + " / " + str(pcbnew.ToMM(ViaDimension.m_Drill)))
                """
                if ViaDimension.m_Diameter == pcbnew.FromMM(0.6): #初期設定
                    self.dlg.lstDefinedViaSizes.SetSelection(index - 1)
                """
        self.dlg.lstDefinedViaSizes.Bind(wx.EVT_CHOICE, self.lstDefinedViaSizesOnChoice) #定義済みビアサイズが選択されたときに関数を呼び出す
        self.dlg.txtViaDiameter.Bind(wx.EVT_TEXT, self.txtViaSizesOnText) #DiameterとHoleどちらのテキストボックスに入力されても呼び出す関数は同じ
        self.dlg.txtViaHole.Bind(wx.EVT_TEXT, self.txtViaSizesOnText)
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #有効レイヤーの取得と登録---------------------------------------------------------------------------------------------------------------------------
        for LayerID in range(32): #IDが0から31のレイヤーのうち有効なものを登録
            if board.IsLayerEnabled(LayerID):
                self.dlg.lstStartLayer.Append(board.GetLayerName(LayerID))
                self.dlg.lstEndLayer.Append(board.GetLayerName(LayerID))
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #内層アニュラリングの選択肢を登録する----------------------------------------------------------------------------------------------------------------
        self.dlg.lstAnnularRings.Append("All copper layers")
        self.dlg.lstAnnularRings.Append("Start, end, and connected layers")
        #self.dlg.lstAnnularRings.Append("Connected layers only") #これの設定方法は不明
        self.dlg.lstAnnularRings.SetSelection(0) #レイヤーペアが隣接していないときでもAll copper layersを初期設定とするため記述が必要
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #ビアタイプを登録し初期設定をThroughとする-----------------------------------------------------------------------------------------------------------
        self.dlg.lstViaType.Append("Through")
        self.dlg.lstViaType.Append("Micro")
        self.dlg.lstViaType.Append("Blind/buried")
        self.dlg.lstViaType.SetSelection(0)
        self.dlg.lstViaType.Bind(wx.EVT_CHOICE, self.lstViaTypeOnChoice) #ビアタイプが選択されたときに関数を呼び出す
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #ビアタイプの初期設定がthroughならばF.CuとB.Cuをレイヤーペアの初期設定としてグレーアウトしさらにそれらの隣接判定を行う-------------------------------------
        self.checkViaTypeAndSetLayerPair() #through以外ならばレイヤーペアは設定されないし隣接判定も行われない

        self.dlg.lstStartLayer.Bind(wx.EVT_CHOICE, self.lstLayerPairOnChoice) #レイヤーペア変更時に隣接判定を行う
        self.dlg.lstEndLayer.Bind(wx.EVT_CHOICE, self.lstLayerPairOnChoice)
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        self.OKButtonControl()
        if self.dlg.ShowModal() == wx.ID_OK: #ダイアログ表示中はdlg.ShowModal()は終了しない
            #netの読み込み 選択していないとネット無しになるがエラーは無い
            ViaNetName = self.dlg.lstViaNet.GetStringSelection()

            #ビアのネットの自動更新の有無 自動更新無しがTrue
            ViaIsFree = not self.dlg.chkUpdateViaNet.IsChecked()

            #ビアタイプ読み込み 何かしらが必ず選択されている
            ViaTypeList = [pcbnew.VIATYPE_THROUGH,pcbnew.VIATYPE_MICROVIA, pcbnew.VIATYPE_BLIND_BURIED,pcbnew.VIATYPE_NOT_DEFINED]
            ViaType = ViaTypeList[self.dlg.lstViaType.GetSelection()]

            #配線とビアのクリアランスの読み込み--------------------------------------------------------------------------------------------------------------
            if self.dlg.chkUseZoneClearance.IsChecked():
                #Use zone clearanceにチェック時は導体ゾーンのクリアランスを使用
                TrackToViaClearance = self.ZoneClearanceList[self.dlg.lstViaNet.GetSelection()]
            else:
                #無効時はテキストボックスから テキストボックスを編集するとチェックが外れる
                TrackToViaClearance = pcbnew.FromMM(float(self.dlg.txtTrackToViaClearance.GetValue()))
            #---------------------------------------------------------------------------------------------------------------------------------------------

            #ビアサイズの読み込み---------------------------------------------------------------------------------------------------------------------------
            if self.dlg.lstDefinedViaSizes.GetSelection() != wx.NOT_FOUND:
                #定義済みサイズが選択されているときはリストから 割り込みにより定義済みサイズが選択されると同時にテキストボックスにも同じサイズが書き込まれる
                ViaDiameter = self.ViasDimensionsList[self.dlg.lstDefinedViaSizes.GetSelection() + 1].m_Diameter #テキストにも書き込まれているが変換されてるので元の値を使う
                ViaDrill    = self.ViasDimensionsList[self.dlg.lstDefinedViaSizes.GetSelection() + 1].m_Drill
            else:
                #選択されていないときはテキストボックスから テキストボックスを編集すると選択が解除されてwx.NOT_FOUNDになる
                ViaDiameter = pcbnew.FromMM(float(self.dlg.txtViaDiameter.GetValue()))
                ViaDrill    = pcbnew.FromMM(float(self.dlg.txtViaHole.GetValue()))
            #---------------------------------------------------------------------------------------------------------------------------------------------

            #レイヤーペアの読み込み 何かしらが必ず選択されている-----------------------------------------------------------------------------------------------
            ViaStartLayerID = board.GetLayerID(self.dlg.lstStartLayer.GetStringSelection()) #LayerIDを保持するのは大変なのでレイヤー名だけ保持してここでIDに変換
            ViaEndLayerID   = board.GetLayerID(self.dlg.lstEndLayer.GetStringSelection())   #StartとEndのレイヤーの上下が逆の場合はKiCadが戻してくれる
            #---------------------------------------------------------------------------------------------------------------------------------------------

            #内層アニュラリングの除去の有無------------------------------------------------------------------------------------------------------------------
            ViaRemoveUnconnectedAnnularRing = bool(self.dlg.lstAnnularRings.GetSelection()) #0=All copper layers=False, 1=True
            #---------------------------------------------------------------------------------------------------------------------------------------------

            #選択中の配線の取得とビアの配置------------------------------------------------------------------------------------------------------------------
            ViaPositionList = []
            selectedTrackList = [track for track in board.GetTracks() if track.IsSelected()]
            for selectedTrack in selectedTrackList:
                TrackStart = selectedTrack.GetStart()
                TrackEnd = selectedTrack.GetEnd()
                TrackWidth = selectedTrack.GetWidth()
                TrackLength = selectedTrack.GetLength()

                offset = TrackWidth//2 + ViaDiameter//2 + TrackToViaClearance #python3においては//で切り捨て除算

                if selectedTrack.GetClass() == "PCB_TRACK":
                    DX = TrackEnd.x - TrackStart.x #整数
                    DY = TrackEnd.y - TrackStart.y
                    sin = -DY/TrackLength #0to1
                    cos = DX/TrackLength
                    dx = int(offset*sin) #整数
                    dy = int(offset*cos)

                    ViaNum = 1 + int(TrackLength/ViaDiameter) #何故か//を使うとViaNumがfloatになり動作せず

                    for step in range(ViaNum):
                        if ViaNum == 1: #stepが0の場合のみ
                            x_temp = TrackStart.x #ビアを1個しか置けなくても置く 1個だけ置かれてるのは見れば分かるのでエラーは出さない
                            y_temp = TrackStart.y
                        else: #配線が短くてViaが1個しか置けないとゼロ除算になるのを回避する
                            x_temp = TrackStart.x + step * int(DX / (ViaNum - 1)) #+=を使う方法より分かりやすい
                            y_temp = TrackStart.y + step * int(DY / (ViaNum - 1))

                        self.AppendPosition(ViaPositionList, [x_temp - dx, y_temp - dy])
                        self.AppendPosition(ViaPositionList, [x_temp + dx, y_temp + dy])

                elif selectedTrack.GetClass() == "PCB_ARC":
                    TrackCenter = selectedTrack.GetCenter() #回転中心
                    TrackRadius = selectedTrack.GetRadius() #半径

                    InnerRadius = TrackRadius - offset
                    OuterRadius = TrackRadius + offset
                    angle_d     = selectedTrack.GetAngle().AsRadians()
                    angle_start = selectedTrack.GetArcAngleStart().AsRadians()

                    if offset > TrackRadius: #円弧半径が小さすぎて内側にビアを置くとクリアランスが保てない場合
                        InnerViaNum = 0 #内側にビアを置かない
                    elif ViaDiameter**2 > 4*InnerRadius**2: #acosが範囲外エラーになる条件
                        InnerViaNum = 1
                    else:
                        InnerViaNum = 1 + int(abs(angle_d)/math.acos(1 - ViaDiameter**2/(2*InnerRadius**2))) #何故か//を使うとViaNumがfloatになり動作せず

                    OuterViaNum = 1 + int(abs(angle_d)/math.acos(1 - ViaDiameter**2/(2*OuterRadius**2))) #ここのangle_dは絶対値でないといけない

                    #内側に置けない場合でも外側に置けるなら置く
                    for step in range(InnerViaNum):
                        if InnerViaNum == 1:
                            angle_temp = angle_start
                        else:
                            angle_temp = angle_start + step * angle_d / (InnerViaNum - 1) #ここのangle_dは正負問わない

                        self.AppendPosition(ViaPositionList, [TrackCenter.x + int(InnerRadius*math.cos(angle_temp)), TrackCenter.y + int(InnerRadius*math.sin(angle_temp))])
                    for step in range(OuterViaNum):
                        if OuterViaNum == 1:
                            angle_temp = angle_start
                        else:
                            angle_temp = angle_start + step * angle_d / (OuterViaNum - 1)

                        self.AppendPosition(ViaPositionList, [TrackCenter.x + int(OuterRadius*math.cos(angle_temp)), TrackCenter.y + int(OuterRadius*math.sin(angle_temp))])

            for ViaPosition in ViaPositionList: #リストにある座標にビアを配置
                self.CreateVia(board, ViaPosition, ViaDiameter, ViaDrill, ViaNetName, ViaIsFree, ViaType, ViaStartLayerID, ViaEndLayerID, ViaRemoveUnconnectedAnnularRing)
            pcbnew.Refresh()

        self.dlg.Destroy()