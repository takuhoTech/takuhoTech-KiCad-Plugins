import pcbnew
import os
import math

class SquareTrackAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "SquareTrackGenerator by takuhoTech"
        self.category = "Modify PCB"
        self.description = "Change selected tracks to square-ended"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "SquareTrackGenerator.png")
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()

        selectedTracks = []

        for track in board.GetTracks():
            if track.IsSelected():
                selectedTracks.append(track)

        length = len(selectedTracks)

        for i in range(length):
            start = selectedTracks[i].GetStart()
            end = selectedTracks[i].GetEnd()
            width = selectedTracks[i].GetWidth()
            length = selectedTracks[i].GetLength()

            layer = selectedTracks[i].GetLayer()#レイヤーを取得
            #layer = board.GetLayerID(selectedTracks[i].GetLayerName())#レイヤーを取得（別解）
            #layer = selectedTracks[i].GetLayerSet()#謎
            net = selectedTracks[i].GetNet()#ネットを取得

            board.Remove(selectedTracks[i])#元の配線を削除

            #矩形生成（斜めにできないため没）
            '''
            rect = pcbnew.PCB_SHAPE(board)
            rect.SetShape(pcbnew.SHAPE_T_RECTANGLE)

            X1 = start.x
            Y1 = int(start.y - width/2)
            X2 = end.x
            Y2 = int(end.y + width/2)

            rect.SetStart(pcbnew.VECTOR2I(X1,Y1))
            rect.SetEnd(pcbnew.VECTOR2I(X2,Y2))

            rect.SetWidth(0)
            rect.SetFilled(True)

            rect.SetLayer(layer)# layer設定
            rect.SetNet(net)#ネット設定
            board.Add(rect)
            '''
            #座標計算
            sin = -(end.y - start.y)/length#y軸の正方向が上か下かで符号が変わる？
            cos = (end.x - start.x)/length
            dx = int((width/2)*sin)
            dy = int((width/2)*cos)

            X1 = start.x - dx
            X2 = start.x + dx
            X3 = end.x + dx
            X4 = end.x - dx

            Y1 = start.y - dy#下向きが正
            Y2 = start.y + dy
            Y3 = end.y + dy
            Y4 = end.y - dy

            pts = [
                (X1,Y1),
                (X2,Y2),
                (X3,Y3),
                (X4,Y4)
            ]
            #ポリゴン生成
            polySet = pcbnew.SHAPE_POLY_SET()
            chain = pcbnew.SHAPE_LINE_CHAIN()
            for (x,y) in pts:
                chain.Append(x, y)
            chain.SetClosed(True)
            polySet.AddOutline(chain)

            poly = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_POLY)
            poly.SetPolyShape(polySet)
            poly.SetWidth(0)
            poly.SetFilled(True)

            poly.SetLayer(layer)# layer設定
            poly.SetNet(net)#ネット設定
            board.Add(poly)

        pcbnew.Refresh()

SquareTrackAction().register()