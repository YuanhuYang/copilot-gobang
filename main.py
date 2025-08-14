"""五子棋 (Gobang) 控制台入口。

提供命令行参数解析、人机/人人对弈循环、命令处理 (落子/AI/悔棋/保存/显示)。
"""
#!/usr/bin/env python3
import argparse
from gobang.game import Game
from gobang.board import Stone
from gobang.ai import SimpleAI


def parse_args():
    """解析命令行参数。"""
    p = argparse.ArgumentParser(description='五子棋 (Gobang) 控制台')
    p.add_argument('--size', type=int, default=15, help='棋盘大小 (默认15)')
    p.add_argument('--mode', choices=['pvp','pve'], default='pve', help='模式: pvp 人人, pve 人机')
    p.add_argument('--load', type=str, help='载入保存的对局文件')
    return p.parse_args()


def show_help():
    """打印交互命令帮助。"""
    print('命令:')
    print('  move r c   落子 (行 列)')
    print('  ai         让 AI 落子 (仅 pve 且轮到 AI 时可省略, AI 也会自动)')
    print('  undo       悔棋一手')
    print('  save file  保存对局到文件')
    print('  show       显示棋盘')
    print('  help       显示帮助')
    print('  exit       退出')


def main():
    """程序入口: 初始化游戏并进入命令循环。"""
    args = parse_args()
    if args.load:
        game = Game.load(args.load)
        print(f'已载入对局 文件={args.load} 尺寸={game.board.size}')
    else:
        game = Game(args.size)
    ai = None
    if args.mode == 'pve':
        # AI 默认执白 (后手)；如果用户希望 AI 先手，可扩展参数
        ai = SimpleAI(Stone.WHITE)
    print('开始五子棋对局. 当前轮到:', '黑(B)' if game.current==Stone.BLACK else '白(W)')
    print(game.board.to_string())
    show_help()

    while True:
        if game.finished:
            w = game.winner()
            if w:
                print('胜者:', '黑(B)' if w==Stone.BLACK else '白(W)')
            else:
                print('平局 (棋盘已满)')
            break

        # AI 自动走
        if ai and game.current == ai.stone:
            mv = ai.best_move(game.board)
            if mv:
                r,c = mv
                try:
                    game.move(r,c)
                    print(f'AI 落子: {r} {c}')
                except Exception as e:  # noqa: BLE001 保持简单交互输出
                    print('AI 落子失败:', e)
            print(game.board.to_string())
            continue

        try:
            cmd = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n退出')
            break
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()
        if op == 'move' and len(parts)==3:
            try:
                r = int(parts[1]); c = int(parts[2])
                game.move(r,c)
                print(game.board.to_string())
                print('下一手:', '黑(B)' if game.current==Stone.BLACK else '白(W)')
            except Exception as e:  # noqa: BLE001
                print('落子失败:', e)
        elif op == 'ai' and ai:
            if game.current != ai.stone:
                print('现在不是 AI 的回合')
            else:
                mv = ai.best_move(game.board)
                if mv:
                    try:
                        game.move(*mv)
                        print(f'AI 落子: {mv[0]} {mv[1]}')
                    except Exception as e:  # noqa: BLE001
                        print('AI 落子失败:', e)
                print(game.board.to_string())
        elif op == 'undo':
            if game.undo():
                print('已悔棋。当前轮到:', '黑(B)' if game.current==Stone.BLACK else '白(W)')
                print(game.board.to_string())
            else:
                print('无法悔棋')
        elif op == 'save' and len(parts)==2:
            try:
                game.save(parts[1])
                print('已保存')
            except Exception as e:  # noqa: BLE001
                print('保存失败:', e)
        elif op == 'show':
            print(game.board.to_string())
        elif op == 'help':
            show_help()
        elif op == 'exit':
            print('退出')
            break
        else:
            print('未知命令, 输入 help 查看')

if __name__ == '__main__':
    main()
