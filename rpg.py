import random
import sys
import time

def slow_print(text, delay=0.04):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def time_gauge_bar(elapsed, total=60, bar_length=10):
    remain = max(0, total - int(elapsed))
    filled = int(bar_length * remain / total)
    bar = '■' * filled + '□' * (bar_length - filled)
    return f"残り時間：{bar} {remain}秒"

class Hero:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.next_exp = 3
        self.max_hp = 100
        self.player_hp = self.max_hp
        self.player_weapon = "素手"
        self.weapon_val = 10
        self.skill_used = False

    def gain_exp(self, amount):
        self.exp += amount
        slow_print(f"経験値を{amount}獲得！")
        levelup_count = 0
        levelup_info = []
        while self.exp >= self.next_exp:
            self.exp -= self.next_exp
            self.level_up(show_message=False)
            levelup_info.append((self.level, self.hp_up, self.weapon_val_up, self.player_hp, self.max_hp, self.next_exp))
            levelup_count += 1
            self.skill_used = False
        if levelup_count > 0:
            for i, info in enumerate(levelup_info):
                level, hp_up, weapon_val_up, player_hp, max_hp, next_exp = info
                slow_print(f"レベルアップ！ 現在のレベル: {level}")
                slow_print(f"HPが{hp_up}上昇、攻撃力が{weapon_val_up}上昇！")
                slow_print(f"HPが全回復！ HP: {player_hp}/{max_hp}")
                slow_print(f"次のレベルまで: {next_exp} 経験値")
        slow_print(f"現在の経験値: {self.exp}/{self.next_exp}")
        slow_print(f"次のレベルまで: {self.next_exp - self.exp} 経験値")

    def level_up(self, show_message=True):
        self.level += 1
        self.hp_up = round(3 * (1 + self.level * 0.3))
        self.max_hp += self.hp_up
        self.player_hp = self.max_hp
        self.weapon_val_up = round(5 * (1 + self.level * 0.3))
        self.weapon_val += self.weapon_val_up
        if self.level == 1:
            self.next_exp = 3
        else:
            self.next_exp = int(3 * (self.level ** 1.5))
        if show_message:
            slow_print(f"レベルアップ！ 現在のレベル: {self.level}")
            slow_print(f"HPが{self.hp_up}上昇、攻撃力が{self.weapon_val_up}上昇！")
            slow_print(f"HPが全回復！ HP: {self.player_hp}/{self.max_hp}")
            slow_print(f"次のレベルまで: {self.next_exp} 経験値")

    def skill(self):
        pass

    def enemy(self, enemy_types):
        self.enemy_type = random.choice(list(enemy_types.keys()))
        self.enemy_hp = enemy_types[self.enemy_type][0]
        self.enemy_attack_val = enemy_types[self.enemy_type][1]
        slow_print(f"{self.enemy_type}が現れた！\nHP: {self.enemy_hp}")

    def attack(self):
        damage = self.weapon_val + random.randint(-5, 5)
        slow_print(f"あなたの{self.player_weapon}攻撃！ {damage}ダメージ！")
        self.enemy_hp -= damage
        if self.enemy_hp < 0:
            self.enemy_hp = 0
        slow_print(f"敵のHP: {self.enemy_hp}")

    def enemy_attack(self):
        damage = self.enemy_attack_val + random.randint(-5, 5)
        slow_print(f"{self.enemy_type}の攻撃！ {damage}ダメージ！")
        self.player_hp -= damage
        if self.player_hp < 0:
            self.player_hp = 0
        slow_print(f"あなたのHP: {self.player_hp}")

    def is_alive(self):
        return self.player_hp > 0

    def is_enemy_alive(self):
        return self.enemy_hp > 0

class Sorder(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "剣"
        self.weapon_val = 20

    def skill(self):
        if not self.skill_used:
            damage = self.weapon_val * 2 + random.randint(0, 10)
            slow_print(f"スキル『渾身の斬撃』発動！ {damage}ダメージ！")
            self.enemy_hp -= damage
            if self.enemy_hp < 0:
                self.enemy_hp = 0
            slow_print(f"敵のHP: {self.enemy_hp}")
            self.skill_used = True
        else:
            slow_print("スキルは既に使用しました。")

class Mage(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "魔法"
        self.weapon_val = 35

    def skill(self):
        if not self.skill_used:
            damage = self.weapon_val * 2 + random.randint(10, 20)
            slow_print(f"スキル『ファイアボール』発動！ {damage}ダメージ！")
            self.enemy_hp -= damage
            if self.enemy_hp < 0:
                self.enemy_hp = 0
            slow_print(f"敵のHP: {self.enemy_hp}")
            self.skill_used = True
        else:
            slow_print("スキルは既に使用しました。")

class Necromancer(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "死霊術"
        self.weapon_val = 15
        self.allies = []

    def attack(self):
        total_damage = self.weapon_val + random.randint(-5, 5)
        slow_print(f"あなたの{self.player_weapon}攻撃！ {total_damage}ダメージ！")
        self.enemy_hp -= total_damage
        if self.enemy_hp < 0:
            self.enemy_hp = 0
        slow_print(f"敵のHP: {self.enemy_hp}")
        # 仲間がいれば加勢
        if self.allies:
            slow_print("仲間が加勢！")
            for ally in self.allies:
                ally_damage = ally['attack'] + random.randint(-2, 2)
                slow_print(f"{ally['name']}の攻撃！ {ally_damage}ダメージ！")
                self.enemy_hp -= ally_damage
                if self.enemy_hp < 0:
                    self.enemy_hp = 0
                slow_print(f"敵のHP: {self.enemy_hp}")

class RPG:
    def __init__(self, enemy_types, player=None):
        self.enemy_types = enemy_types
        if player is None:
            self.player = self.choose_job()
        else:
            self.player = player
        self.player.enemy(self.enemy_types)

    def choose_job(self):
        while True:
            slow_print("ジョブを選択してください：")
            slow_print("1: 剣士")
            slow_print("2: 魔法使い")
            choice = input("番号を入力: ")
            if choice == "1":
                slow_print("剣士を選択しました。\n")
                return Sorder()
            elif choice == "2":
                slow_print("魔法使いを選択しました。\n")
                return Mage()
            elif choice == "111":
                slow_print("シークレットジョブ『ネクロマンサー』を選択しました…！\n")
                return Necromancer()
            else:
                slow_print("無効な入力です。もう一度入力してください。\n")

    def battle(self, enemy_types):
        slow_print("\n=== RPG戦闘システム ===")
        while self.player.is_alive() and self.player.is_enemy_alive():
            slow_print(f"\nあなたのレベル: {self.player.level}")
            slow_print(f"あなたのHP: {self.player.player_hp}")
            slow_print(f"敵のHP: {self.player.enemy_hp}")
            if not self.player.skill_used:
                slow_print("1: 通常攻撃  2: スキル（1回のみ）")
                action = input("行動を選択してください: ")
                if action == "2":
                    self.player.skill()
                else:
                    self.player.attack()
            else:
                slow_print("1: 通常攻撃")
                action = input("行動を選択してください: ")
                self.player.attack()
            if not self.player.is_enemy_alive():
                slow_print(f"\n{self.player.enemy_type}を倒した！")
                exp_gain = enemy_types[self.player.enemy_type][2]
                self.player.gain_exp(exp_gain)
                if isinstance(self.player, Necromancer):
                    ally = {
                        'name': self.player.enemy_type,
                        'hp': int(self.player.enemy_hp // 2),
                        'attack': int(self.player.enemy_attack_val // 2)
                    }
                    self.player.allies.append(ally)
                    slow_print(f"{self.player.enemy_type}が仲間になった！（HP:{ally['hp']} 攻撃:{ally['attack']}）")
                break
            self.player.enemy_attack()
            if not self.player.is_alive():
                slow_print("\nあなたは倒れてしまった…")
                break
        self.player.player_hp = 100 + (self.player.level - 1) * 3 * (1 + self.player.level * 0.3)

def save_score(mode, name, score):
    with open('score.txt', 'a', encoding='utf-8') as f:
        f.write(f"{mode},{name},{score}\n")

def main():
    enemy_types = {"スライム": [30, 10, 3], "ゴブリン": [50, 15, 5], "ゾンビ": [70, 20, 7], "ドラゴン": [100, 25, 10]}
    player = None
    slow_print("モードを選択してください：")
    slow_print("1: タイムアタック（1分間に何体倒せるか）")
    slow_print("2: レベルチャレンジ（ひたすらレベルをあげる）")
    while True:
        mode_choice = input("番号を入力: ")
        if mode_choice == "1":
            mode = "タイムアタック"
            break
        elif mode_choice == "2":
            mode = "レベルチャレンジ"
            break
        else:
            slow_print("無効な入力です。もう一度入力してください。\n")
    if mode == "タイムアタック":
        import time
        player = None
        start_time = time.time()
        count = 0
        while True:
            elapsed = time.time() - start_time
            slow_print(time_gauge_bar(elapsed))
            game = RPG(enemy_types, player)
            game.battle(enemy_types)
            player = game.player
            player.player_hp = player.max_hp
            count += 1
            if player.player_hp <= 0:
                slow_print("HPが0になりました。ゲームオーバーです。")
                break
            if time.time() - start_time > 60:
                slow_print("1分経過！タイムアタック終了！")
                break
        slow_print(f"倒した数: {count}")
        name = input("プレイヤーネームを入力してください: ")
        save_score(mode, name, count)
    else:
        player = None
        while True:
            game = RPG(enemy_types, player)
            game.battle(enemy_types)
            player = game.player
            player.player_hp = player.max_hp
            if player.player_hp <= 0:
                slow_print("HPが0になりました。ゲームオーバーです。")
                slow_print("復活しますか？ (y/n)")
                revive = input().lower()
                if revive == 'y':
                    player.player_hp = player.max_hp
                    slow_print("HPが全回復しました！")
                    continue
                else:
                    break
            slow_print("\nもう一度プレイしますか？")
            choice = input("y/n: ")
            if choice.lower() != 'y':
                break
        slow_print(f"最終レベル: {player.level}")
        name = input("プレイヤーネームを入力してください: ")
        save_score(mode, name, player.level)
    slow_print("ゲーム終了")
    slow_print('Thank you for playing!')

main()
