 import random
import sys
import time
import string

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
        self.enemies = []  # 複数エネミー管理

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
            self.skill_used = False  # レベルアップ時にスキル再使用可能
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
        self.player_hp = self.max_hp  # レベルアップ時に全回復
        self.weapon_val_up = round(5 * (1 + self.level * 0.3))
        self.weapon_val += self.weapon_val_up
        if self.level == 1:
            self.next_exp = 3
        else:
            self.next_exp = int(3 * (self.level ** 1.5))
        # レベル15でジョブアップ（能力上昇後に実行）
        if self.level == 15:
            self.job_up()
        if show_message:
            slow_print(f"レベルアップ！ 現在のレベル: {self.level}")
            slow_print(f"HPが{self.hp_up}上昇、攻撃力が{self.weapon_val_up}上昇！")
            slow_print(f"HPが全回復！ HP: {self.player_hp}/{self.max_hp}")
            slow_print(f"次のレベルまで: {self.next_exp} 経験値")

    def job_up(self):
        if isinstance(self, Sorder):
            slow_print("ジョブアップ！")
            self.job = "勇者"
        elif isinstance(self, Mage):
            slow_print("ジョブアップ！")
            self.job = "大魔法使い"
        elif isinstance(self, Necromancer):
            slow_print("ジョブアップ！")
            self.job = "影の君主"
        # 攻撃力を1.5倍に強化
        self.weapon_val = int(self.weapon_val * 1.5)
        slow_print(f"攻撃力が大幅に上昇！ 現在の攻撃力: {self.weapon_val}")

    def skill(self):
        # 継承先で実装
        pass

    def enemy(self, enemy_types, battle_count=0, difficulty="NORMAL"):
        self.enemies = []
        # 難易度に応じて敵の数を調整
        if difficulty == "EASY":
            num_enemies = random.randint(1, 2)
        else:  # NORMAL, HARD
            num_enemies = random.randint(1, 3)

        enemy_names = random.choices(list(enemy_types.keys()), k=num_enemies)
        for i, name in enumerate(enemy_names):
            suffix = string.ascii_uppercase[i]
            enemy_name = f"{name}{suffix}"
            base_hp, base_attack, _ = enemy_types[name]
            # ステータス補正
            bonus = int(battle_count * 1.15)
            hp = base_hp + bonus
            attack = base_attack + bonus

            # HARD難易度ではステータス1.3倍
            if difficulty == "HARD":
                hp = int(hp * 1.3)
                attack = int(attack * 1.3)

            self.enemies.append({
                'type': name,
                'name': enemy_name,
                'hp': hp,
                'attack': attack
            })
            slow_print(f"{enemy_name}が現れた！")

    def attack(self):
        # 単体攻撃: 生存している敵をA→B→Cの順で自動攻撃
        alive = [e for e in self.enemies if e['hp'] > 0]
        if not alive:
            return
        target = alive[0]  # 先頭（A→B→C順）
        damage = self.weapon_val + random.randint(-5, 5)
        slow_print(f"あなたの{self.player_weapon}攻撃！ {target['name']}に{damage}ダメージ！")
        target['hp'] -= damage
        if target['hp'] < 0:
            target['hp'] = 0
        slow_print(f"{target['name']}のHP: {target['hp']}\n")

    def enemy_attack(self):
        slow_print("敵の攻撃！")
        # 通常: プレイヤーのみ攻撃
        if not isinstance(self, Necromancer):
            for e in self.enemies:
                if e['hp'] > 0:
                    damage = e['attack'] + random.randint(-5, 5)
                    slow_print(f"{e['name']}の攻撃！ {damage}ダメージ！")
                    self.player_hp -= damage
                    if self.player_hp < 0:
                        self.player_hp = 0
                    slow_print(f"あなたのHP: {self.player_hp}")
        else:
            # ネクロマンサー: プレイヤー＋味方全員に攻撃
            for e in self.enemies:
                if e['hp'] > 0:
                    damage = e['attack'] + random.randint(-5, 5)
                    slow_print(f"{e['name']}の攻撃！ {damage}ダメージ！")
                    self.player_hp -= damage
                    if self.player_hp < 0:
                        self.player_hp = 0
                    slow_print(f"あなたのHP: {self.player_hp}")
                    # 味方にもダメージ
                    for ally in self.allies:
                        ally['hp'] -= damage
                    # HP0以下の味方を消滅
                    before = len(self.allies)
                    self.allies = [a for a in self.allies if a['hp'] > 0]
                    after = len(self.allies)
                    if before > after:
                        slow_print(f"{before - after}体の死霊が消滅した…")

    def is_alive(self):
        return self.player_hp > 0

    def is_enemy_alive(self):
        return any(e['hp'] > 0 for e in self.enemies)

class Sorder(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "剣"
        self.weapon_val = 20
        self.job = "剣士"

    def skill(self):
        if self.skill_used:
            slow_print("スキルは既に使用しました。")
            return
        # 全体攻撃
        for e in self.enemies:
            if e['hp'] > 0:
                damage = self.weapon_val * 2 + random.randint(0, 10)
                slow_print(f"スキル『渾身の斬撃』発動！ {e['name']}に{damage}ダメージ！")
                e['hp'] -= damage
                if e['hp'] < 0:
                    e['hp'] = 0
                slow_print(f"{e['name']}のHP: {e['hp']}")
        self.skill_used = True

class Mage(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "魔法"
        self.weapon_val = 35
        self.job = "魔法使い"

    def skill(self):
        if self.skill_used:
            slow_print("スキルは既に使用しました。")
            return
        # 全体攻撃
        for e in self.enemies:
            if e['hp'] > 0:
                damage = self.weapon_val * 2 + random.randint(10, 20)
                slow_print(f"スキル『ファイアボール』発動！ {e['name']}に{damage}ダメージ！")
                e['hp'] -= damage
                if e['hp'] < 0:
                    e['hp'] = 0
                slow_print(f"{e['name']}のHP: {e['hp']}")
        self.skill_used = True

class Necromancer(Hero):
    def __init__(self):
        super().__init__()
        self.player_weapon = "死霊術"
        self.weapon_val = 15
        self.job = "ネクロマンサー"
        self.allies = []  # 仲間リスト（倒した敵）
        self.ally_buffed = False  # 死霊強化済みフラグ

    def attack(self):
        # 単体攻撃: 生存している敵をA→B→Cの順で自動攻撃
        alive = [e for e in self.enemies if e['hp'] > 0]
        if not alive:
            return
        target = alive[0]
        total_damage = self.weapon_val + random.randint(-5, 5)
        slow_print(f"あなたの{self.player_weapon}攻撃！ {target['name']}に{total_damage}ダメージ！")
        target['hp'] -= total_damage
        if target['hp'] < 0:
            target['hp'] = 0
        slow_print(f"{target['name']}のHP: {target['hp']}")
        # 仲間がいれば加勢
        if self.allies:
            slow_print("仲間が加勢！")
            for ally in self.allies:
                ally_damage = ally['attack'] + random.randint(-2, 2)
                slow_print(f"{ally['name']}の攻撃！ {ally_damage}ダメージ！")
                target['hp'] -= ally_damage
                if target['hp'] < 0:
                    target['hp'] = 0
                slow_print(f"{target['name']}のHP: {target['hp']}")

    def skill(self):
        if self.skill_used:
            slow_print("スキルは既に使用しました。")
            return
        # 死霊の奔流：全体大ダメージ＋死霊強化
        for e in self.enemies:
            if e['hp'] > 0:
                base_damage = int(self.weapon_val * 2.5 + len(self.allies) * 10)
                slow_print(f"スキル『死霊の奔流』発動！ {e['name']}に{base_damage}ダメージ！")
                e['hp'] -= base_damage
                if e['hp'] < 0:
                    e['hp'] = 0
                slow_print(f"{e['name']}のHP: {e['hp']}")
        if not self.ally_buffed:
            self.ally_buffed = True
            slow_print("これから仲間になる死霊たちの力が高まる！（攻撃・HPが1.2倍）\n")
        self.skill_used = True

class RPG:
    def __init__(self, enemy_types, player=None, battle_count=0, difficulty="NORMAL"):
        self.enemy_types = enemy_types
        self.battle_count = battle_count
        self.difficulty = difficulty
        if player is None:
            self.player = self.choose_job()
        else:
            self.player = player
        self.player.enemy(self.enemy_types, self.battle_count, self.difficulty)

    def choose_job(self):
        while True:
            slow_print("ジョブを選択してください：")
            slow_print("1: 剣士")
            slow_print("2: 魔法使い")
            # シークレットジョブは表示しない
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
        self.battle_count += 1
        slow_print("\n=== RPG戦闘システム ===")
        while self.player.is_alive() and self.player.is_enemy_alive():
            slow_print(f"\nあなたのレベル: {self.player.level} ({self.player.job})")
            slow_print(f"あなたのHP: {self.player.player_hp}")
            for e in self.player.enemies:
                if e['hp'] > 0:
                    slow_print(f"{e['name']} HP: {e['hp']}")
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
            # ここから個別撃破ごとに経験値処理
            for e in self.player.enemies:
                if 'defeated' not in e and e['hp'] <= 0:
                    slow_print(f"\n{e['name']}を倒した！")
                    exp_gain = enemy_types[e['type']][2]
                    self.player.gain_exp(exp_gain)
                    e['defeated'] = True
                    # ネクロマンサーなら仲間に追加
                    if isinstance(self.player, Necromancer):
                        hp = int(enemy_types[e['type']][0] // 2)
                        if hp <= 0:
                            hp = 1
                        attack = int(enemy_types[e['type']][1] // 2)
                        if getattr(self.player, 'ally_buffed', False):
                            hp = int(hp * 1.2)
                            attack = int(attack * 1.2)
                        ally = {
                            'name': e['name'],
                            'hp': hp,
                            'attack': attack
                        }
                        self.player.allies.append(ally)
                        slow_print(f"{e['name']}が仲間になった！（HP:{ally['hp']} 攻撃:{ally['attack']}）\n")
            if not self.player.is_enemy_alive():
                break
            self.player.enemy_attack()
            if not self.player.is_alive():
                slow_print("\nあなたは倒れてしまった…\n")
                break
        self.player.player_hp = 100 + (self.player.level - 1) * 3 * (1 + self.player.level * 0.3)

def save_score(mode, name, score):
    with open('score.txt', 'a', encoding='utf-8') as f:
        f.write(f"{mode},{name},{score}\n")

def main():
    enemy_types = {"スライム": [30, 10, 3], "ゴブリン": [50, 15, 5], "ゾンビ": [70, 20, 7], "ドラゴン": [100, 25, 10]}
    player = None

    # 難易度選択
    slow_print("難易度を選択してください：")
    slow_print("1: EASY（敵1~2体）")
    slow_print("2: NORMAL（敵1~3体）")
    slow_print("3: HARD（敵1~3体、ステータス1.3倍）")
    while True:
        difficulty_choice = input("番号を入力: ")
        if difficulty_choice == "1":
            difficulty = "EASY"
            break
        elif difficulty_choice == "2":
            difficulty = "NORMAL"
            break
        elif difficulty_choice == "3":
            difficulty = "HARD"
            break
        else:
            slow_print("無効な入力です。もう一度入力してください。\n")

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
            game = RPG(enemy_types, player, battle_count=count, difficulty=difficulty)
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
        auto_continue = False
        battle_count = 0
        while True:
            game = RPG(enemy_types, player, battle_count=battle_count, difficulty=difficulty)
            game.battle(enemy_types)
            player = game.player
            player.player_hp = player.max_hp
            battle_count += 1
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
            if not auto_continue:
                slow_print("\n続けてプレイしますか？")
                slow_print("1: 続ける  2: やめる  3: 今後自動で続ける")
                while True:
                    choice = input("番号を入力: ")
                    if choice == '1':
                        break
                    elif choice == '2':
                        return_end = True
                        break
                    elif choice == '3':
                        auto_continue = True
                        break
                    else:
                        slow_print("無効な入力です。もう一度入力してください。")
                if 'return_end' in locals() and return_end:
                    break
        slow_print(f"最終レベル: {player.level}")
        name = input("プレイヤーネームを入力してください: ")
        save_score(mode, name, player.level)
    slow_print("ゲーム終了")
    slow_print('Thank you for playing!')
    slow_print("Made by tk.")
    slow_print("隠し要素を探してみてね！")


main()
