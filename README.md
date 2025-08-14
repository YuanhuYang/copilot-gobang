# 五子棋 (Gobang) 控制台程序

## 功能
- 任意尺寸棋盘 (>=5)，默认 15
- 人人 / 人机 (简单启发式 AI 防守 + 进攻)
- 胜负 / 平局判定（连续五子）
- 悔棋、保存、载入
- 命令行交互，无第三方依赖

## 运行
```bash
python main.py --mode pve --size 15
```
Windows PowerShell 可直接：
```powershell
python .\main.py
```

## 参数
- `--size N` 棋盘大小
- `--mode pvp|pve` 对弈模式
- `--load file` 载入存档

## 交互命令
| 命令 | 说明 |
| ---- | ---- |
| move r c | 在 (r,c) 落子 |
| ai | 让 AI 落子 (pve 模式) |
| undo | 悔棋 |
| save file | 保存对局到文件 |
| show | 显示棋盘 |
| help | 帮助 |
| exit | 退出 |

## 保存格式
简单文本：
```
<size>|r,c,Stone;...
<current>
<winner或空>
```

## 测试
`tests/` 暂留，可添加单元测试：
- Board 落子与胜负判定
- Game 悔棋与保存加载
- AI 合理返回坐标

## 许可
自用示例代码，可自由修改。
