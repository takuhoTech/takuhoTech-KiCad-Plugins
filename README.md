# takuhoTech-KiCad-Plugins
takuhoTech's KiCad Plugins

KiCad 9.0で開発を行っています.

## Square Track Generator

選択中の配線をいい感じにポリゴンに置き換えるプラグインです.

パッドからはみ出している配線の先を引っ込ませることができます.

![Image](https://github.com/user-attachments/assets/b31da635-eab1-48e8-92c6-8c81ea13aed4)

## Via Fence Generator

選択中の配線の横にビアを並べるプラグインです.

屈曲部のある配線に対しては正しくビアを配置できません.

円弧と直線の接続部においてビアが重なって生成される場合があります.

設定ダイアログの挙動はKiCadの「配線とビアのプロパティ」とほぼ同じです.

配線とビアのクリアランスの自動補間が可能です.

![Image](https://github.com/user-attachments/assets/13164859-8306-42ad-b2c1-e3e4a141d07d)

## Grid Origin Aligner

選択したパッドの位置にグリッド原点を配置するプラグインです.

## How to install

KiCadの「プラグイン&コンテンツマネージャー」の「ファイルからインストール」でReleaseからダウンロードしたzipファイルを選択することでインストールが可能です.
