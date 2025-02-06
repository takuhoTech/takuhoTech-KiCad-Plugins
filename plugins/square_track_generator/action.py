import pcbnew
import os
import math
import numpy

class SquareTrackAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Square Track Generator"
        self.category = "Modify PCB"
        self.description = "Change selected tracks to square-ended"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./32x32.png")
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()

        selectedTracks = [track for track in board.GetTracks() if track.IsSelected()]

        for i in range(len(selectedTracks)):
            start = selectedTracks[i].GetStart()
            end = selectedTracks[i].GetEnd()
            width = selectedTracks[i].GetWidth()
            length = selectedTracks[i].GetLength()

            layer = selectedTracks[i].GetLayer() #レイヤーIDを取得
            #layer = board.GetLayerID(selectedTracks[i].GetLayerName())#レイヤーを取得（別解）
            #layer = selectedTracks[i].GetLayerSet()#謎
            net = selectedTracks[i].GetNet() #ネットを取得

            board.Remove(selectedTracks[i]) #元の配線を削除

            #ポリゴン座標
            chain = pcbnew.SHAPE_LINE_CHAIN()

            if selectedTracks[i].GetClass() == 'PCB_TRACK':
                sin = -(end.y - start.y)/length #y軸の正方向が上か下かで符号が変わる？
                cos = (end.x - start.x)/length
                dx = int((width/2)*sin)
                dy = int((width/2)*cos)

                chain.Append(start.x - dx, start.y - dy)
                chain.Append(start.x + dx, start.y + dy)
                chain.Append(end.x   + dx, end.y   + dy)
                chain.Append(end.x   - dx, end.y   - dy)

            elif selectedTracks[i].GetClass() == 'PCB_ARC':
                center      = selectedTracks[i].GetCenter() #回転中心
                radius      = selectedTracks[i].GetRadius() #半径
                angle_disp  = int(selectedTracks[i].GetAngle().AsDegrees()*10)
                angle_start = int(selectedTracks[i].GetArcAngleStart().AsDegrees()*10)
                #angle_end   = selectedTracks[i].GetArcAngleEnd().AsDegrees()

                #1度ずつ打つ処理にすると開始点と終点の角度が整数でないとき精度を保つ処理が面倒なので1/10度ずつ点を打つ
                for t in range(angle_start, angle_start + angle_disp + numpy.sign(angle_disp), numpy.sign(angle_disp)):
                    chain.Append(center.x+int((radius-width/2)*math.cos(math.radians(t/10))),center.y+int((radius-width/2)*math.sin(math.radians(t/10))))
                for t in range(angle_start + angle_disp, angle_start - numpy.sign(angle_disp), -numpy.sign(angle_disp)):
                    chain.Append(center.x+int((radius+width/2)*math.cos(math.radians(t/10))),center.y+int((radius+width/2)*math.sin(math.radians(t/10))))
                #Python3環境ではint/int=float

            chain.SetClosed(True)
            polySet = pcbnew.SHAPE_POLY_SET()
            polySet.AddOutline(chain)

            poly = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_POLY)
            poly.SetPolyShape(polySet)
            poly.SetWidth(0)
            poly.SetFilled(True)

            poly.SetLayer(layer) #layer設定
            poly.SetNet(net) #ネット設定
            board.Add(poly)

        pcbnew.Refresh()
