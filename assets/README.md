投诉管理 Skill 图标资源目录。

- icon.svg：图标矢量源文件（基于参考图"蓝底白盾牌+横线对勾"风格重绘，文字由"消保评价"改为"投诉管理"）
- render_icon.py：用 Pillow 渲染 _icon.png 的脚本（512x512，4x 超采样抗锯齿，字体 Hiragino Sans GB W6）

重新生成图标：python3 render_icon.py（输出到 skill 根目录 _icon.png）
