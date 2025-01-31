import pcbnew
import os
import math

def CreateVia(brd, x, y, diameter, drill, net = "GND", isFree = True, viaType = pcbnew.VIATYPE_THROUGH, layer1 = pcbnew.F_Cu, layer2 = pcbnew.B_Cu, removeUnconnectedAnnularRing = False):
    via = pcbnew.PCB_VIA(brd)
    via.SetPosition(pcbnew.VECTOR2I(x, y))
    via.SetWidth(diameter)       #外径
    via.SetDrill(drill)          #ドリル径

    via.SetNet(brd.FindNet(net)) #ネット
    via.SetIsFree(isFree)        #True=手動でビアを置く場合と同じく自動更新されない False=ビアのネットは置かれた場所によって自動更新される
    via.SetViaType(viaType)         #pcbnew.VIATYPE_THROUGH,pcbnew.VIATYPE_BLIND_BURIED,pcbnew.VIATYPE_MICROVIA,pcbnew.VIATYPE_NOT_DEFINEDのどれか
    via.SetLayerPair(layer1, layer2) #レイヤーペア
    via.SetRemoveUnconnected(removeUnconnectedAnnularRing) #True=始点,終点,および接続されたレイヤー False=すべての導体レイヤー
    
    brd.Add(via)

class ViaFenceAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Via Fence Generator"
        self.category = "Modify PCB"
        self.description = "Add via fence to selected tracks"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./32x32.png")
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()
        selectedTracks = []
        for track in board.GetTracks():
            if track.IsSelected():
                selectedTracks.append(track)
        for i in range(len(selectedTracks)):
            TrackStart = selectedTracks[i].GetStart()
            TrackEnd = selectedTracks[i].GetEnd()
            TrackWidth = selectedTracks[i].GetWidth()
            TrackLength = selectedTracks[i].GetLength()
            #配線のレイヤー情報は不要
            TrackClearance = pcbnew.FromMM(0.2)
            ViaDiameter = pcbnew.FromMM(0.6)
            ViaDrill    = pcbnew.FromMM(0.3)

            offset = TrackWidth//2 + ViaDiameter//2 + TrackClearance #python3においては//で切り捨て除算

            if selectedTracks[i].GetClass() == 'PCB_TRACK':
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

                    CreateVia(board, x_temp - dx, y_temp - dy, ViaDiameter, ViaDrill)
                    CreateVia(board, x_temp + dx, y_temp + dy, ViaDiameter, ViaDrill)

            elif selectedTracks[i].GetClass() == 'PCB_ARC':
                TrackCenter = selectedTracks[i].GetCenter() #回転中心
                TrackRadius = selectedTracks[i].GetRadius() #半径

                InnerRadius = TrackRadius - offset
                OuterRadius = TrackRadius + offset
                angle_d     = selectedTracks[i].GetAngle().AsRadians()
                angle_start = selectedTracks[i].GetArcAngleStart().AsRadians()

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
                    CreateVia(board, TrackCenter.x + int(InnerRadius*math.cos(angle_temp)), TrackCenter.y + int(InnerRadius*math.sin(angle_temp)), ViaDiameter, ViaDrill)

                for step in range(OuterViaNum):
                    if OuterViaNum == 1:
                        angle_temp = angle_start
                    else:
                        angle_temp = angle_start + step * angle_d / (OuterViaNum - 1)
                    CreateVia(board, TrackCenter.x + int(OuterRadius*math.cos(angle_temp)), TrackCenter.y + int(OuterRadius*math.sin(angle_temp)), ViaDiameter, ViaDrill)

        pcbnew.Refresh()
