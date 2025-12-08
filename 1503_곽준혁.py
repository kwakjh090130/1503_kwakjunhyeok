import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))  # 이 파일이 있는 위치
target_folder_path = os.path.join(script_dir, "1503_kwakjunhyeok")

def auto_download_repo():
    zip_url = "https://github.com/kwakjh090130/1503_kwakjunhyeok/archive/refs/heads/main.zip"
    zip_name = os.path.join(script_dir, "repo.zip")  # zip도 이 파일 옆에 다운로드

    extract_temp_folder = os.path.join(script_dir, "1503_kwakjunhyeok-main")

    # 이미 폴더가 있으면 다운로드 스킵
    if os.path.exists(target_folder_path):
        print("이미 설치된 폴더가 있어 스킵합니다.")
        return

    print("ZIP 파일 다운로드 중...")
    urllib.request.urlretrieve(zip_url, zip_name)

    print("압축 해제 중...")
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(script_dir)

    # main 폴더 → target 폴더로 이름 변경
    os.rename(extract_temp_folder, target_folder_path)

    # zip 삭제
    os.remove(zip_name)
    print("완료!")

# 자동 설치 함수
def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} 패키지가 없어 설치합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 필요한 패키지 목록
required_packages = [
    "pygame",
    "numpy"
]

for pkg in required_packages:
    install_if_missing(pkg)
auto_download_repo()
# 이후 원래 코드
import pygame, numpy
import csv, random, math, time, os

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("포켓몬 2인용 싱글배틀")

#base_path = os.path.dirname(os.path.abspath(__file__))+"\\1503_kwakjunhyeok"
font_path = os.path.join(target_folder_path, "malgun.ttf")

font = pygame.font.Font(font_path, 28)
clock = pygame.time.Clock()

type_chart={
    "불꽃":{"풀":2.0,"벌레":2.0,"강철":2.0,"얼음":2.0,"바위":0.5,"불꽃":0.5,"물":0.5,"드래곤":0.5},
    "물":{"땅":2.0,"바위":2.0,"불꽃":2.0,"물":0.5,"풀":0.5,"드래곤":0.5},
    "풀":{"땅":2.0,"바위":2.0,"물":2.0,"독":0.5,"비행":0.5,"벌레":0.5,"불꽃":0.5,"강철":0.5,"풀":0.5,"드래곤":0.5},
    "노말":{"바위":0.5,"강철":0.5,"고스트":0},
    "고스트":{"노말":0,"고스트":2.0,"에스퍼":2.0,"악":0.5},
    "격투":{"노말":2.0,"바위":2.0,"강철":2.0,"얼음":2.0,"악":2.0,"독":0.5,"비행":0.5,"벌레":0.5,"에스퍼":0.5,"페어리":0.5,"고스트":0},
    "독":{"독":0.5,"땅":0.5,"바위":0.5,"고스트":0.5,"풀":2.0,"페어리":2.0,"강철":0},
    "땅":{"독":2.0,"바위":2.0,"강철":2.0,"불꽃":2.0,"전기":2.0,"비행":0,"벌레":0.5,"풀":0.5},
    "비행":{"격투":2.0,"벌레":2.0,"풀":2.0,"바위":0.5,"강철":0.5,"전기":0.5},
    "벌레":{"풀":2.0,"에스퍼":2.0,"악":2.0,"격투":0.5,"독":0.5,"비행":0.5,"고스트":0.5,"강철":0.5,"불꽃":0.5,"페어리":0.5},
    "바위":{"비행":2.0,"벌레":2.0,"불꽃":2.0,"얼음":2.0,"격투":0.5,"땅":0.5,"강철":0.5},
    "강철":{"바위":2.0,"얼음":2.0,"페어리":2.0,"강철":0.5,"불꽃":0.5,"물":0.5,"전기":0.5},
    "전기":{"비행":2.0,"물":2.0,"전기":0.5,"풀":0.5,"드래곤":0.5,"땅":0},
    "얼음":{"땅":2.0,"비행":2.0,"풀":2.0,"드래곤":2.0,"강철":0.5,"불꽃":0.5,"물":0.5,"얼음":0.5},
    "에스퍼":{"격투":2.0,"독":2.0,"강철":0.5,"에스퍼":0.5,"악":0},
    "드래곤":{"강철":0.5,"드래곤":2.0,"페어리":0},
    "악":{"고스트":2.0,"에스퍼":2.0,"격투":0.5,"악":0.5,"페어리":0.5},
    "페어리":{"격투":2.0,"드래곤":2.0,"악":2.0,"독":0.5,"강철":0.5,"불꽃":0.5}
}
qoWkd_type_chart={
    "노말":{"바위":0.5,"강철":0.5},
    "격투":{"노말":2.0,"바위":2.0,"강철":2.0,"얼음":2.0,"악":2.0,"독":0.5,"비행":0.5,"벌레":0.5,"에스퍼":0.5,"페어리":0.5}
}
def load_csv(filename):
    path = os.path.join(target_folder_path, filename)
    with open(path, encoding="cp949") as f:
        reader = csv.DictReader(f)
        return list(reader)


pokemon_data = load_csv("pokemon_data.csv")
moves_data = load_csv("moves.csv")

def find_move(name):
    for m in moves_data:
        if m["name"] == name:
            return m
    return None

page, selected_index = 0, 0
pokemon_per_page = 6
state = "select_pokemon"
current_player = 1

team_1, team_2 = [],[]
battle_team_1, battle_team_2 = [],[]
selected_pokemon = None
selected_for_battle = []

ev_points = [0,0,0,0,0,0]
ev_names = ["HP","Atk","Def","SpA","SpD","Spe"]
ev_index = 0
max_ev_total = 510
input_buffer = ""

iv_points = [0,0,0,0,0,0]
iv_names = ["HP","Atk","Def","SpA","SpD","Spe"]
iv_index=0
max_iv=31

nature = [0,0,0,0,0]
nature_names = ["Atk","Def","SpA","SpD","Spe"]
nature_index = 0

available_moves = []
selected_moves = [""]*3
move_index = 0
move_page = 0
moves_per_page = 8
selected_moves_PP=[]

available_abilities=[]
selected_abilities=None
ability_index = 0

available_items=["생명의구슬","달인의띠","실크스카프","목탄","신비의물방울","기적의씨",
                 "자석","녹지않는얼음","검은띠","독바늘","부드러운모래","예리한부리","휘어진스푼",
                 "은빛가루","딱딱한돌","저주의부적","용의이빨","검은안경","금속코트","요정의깃털",
                 "노말주얼","룸서비스",
                 "방진고글","빛의점토","차가운바위","보송보송바위",
                 "뜨거운바위","축축한바위","그라운드코트"
                 ]
selected_item=None
item_index = 0
item_page = 0
items_per_page = 8

current_turn = 1
p1_hp, p2_hp = 100, 100
p1_move_choice, p2_move_choice = None, None

def draw_text(text, x, y, color=(255,255,255)):
    t = font.render(str(text), True, color)
    screen.blit(t, (x, y))

def draw_text_center(text, y, color=(255,255,255)):
    t = font.render(str(text), True, color)
    rect = t.get_rect(center=(WIDTH//2, y))
    screen.blit(t, rect)

def wait_for_enter(next_state_name, message="다음 화면으로 넘어갑니다. 엔터를 누르세요."):
    global state
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        draw_text_center(message, HEIGHT // 2 - 40, (255, 255, 255))
        draw_text_center("Press ENTER", HEIGHT // 2 + 40, (180, 180, 180))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    state = next_state_name

def draw_select_screen():
    screen.fill((20, 30, 50))
    draw_text_center(f"{current_player}P 포켓몬 선택 (← →로 페이지 이동, Enter 선택)", 50)
    start = page * pokemon_per_page
    for i in range(pokemon_per_page):
        idx = start + i
        if idx >= len(pokemon_data): break
        poke = pokemon_data[idx]["name"]
        color = (255,255,0) if i == selected_index else (200,200,200)
        draw_text(f"{poke}", 150, 150 + i*50, color)
    draw_text_center(f"Page {page+1}/{(len(pokemon_data)-1)//pokemon_per_page+1}", HEIGHT-40)

def draw_iv_setting():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 개체치 분배", 50)
    for i, name in enumerate(iv_names):
        y = 150 + i*50
        color = (255,255,0) if i == iv_index else (255,255,255)
        draw_text(f"{name}: {iv_points[i]}", 400, y, color)
    draw_text_center(f"현재 입력: {input_buffer}", 550, (180,180,180))
    draw_text_center("↑↓: 항목 이동 | ←→: ±10 | 숫자 입력 | Enter: 확정", HEIGHT-40, (180,180,180))

def draw_ev_setting():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 노력치 분배", 50)
    total = sum(ev_points)
    for i, name in enumerate(ev_names):
        y = 150 + i*50
        color = (255,255,0) if i == ev_index else (255,255,255)
        draw_text(f"{name}: {ev_points[i]}", 400, y, color)
    draw_text_center(f"총합 {total}/{max_ev_total}", 500)
    draw_text_center(f"현재 입력: {input_buffer}", 550, (180,180,180))
    draw_text_center("↑↓: 항목 이동 | 숫자 입력 | Enter: 확정", HEIGHT-40, (180,180,180))

def draw_nature_up_select():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 성격에 의한 증가 능력치 선택", 40)
    for i, m in enumerate(nature_names):
        y = 120 + i * 40
        real_index=i
        color = (0,255,255) if real_index == nature_index else (200,200,200)
        draw_text(f"{m}", 300, y, color)
    draw_text_center(f"↑↓: 이동 | Enter: 완료", HEIGHT - 40, (180,180,180))

def draw_nature_down_select():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 성격에 의한 하락 능력치 선택", 40)
    for i, m in enumerate(nature_names):
        y = 120 + i * 40
        real_index=i
        color = (255,0,0) if real_index == nature_index else (200,200,200) if not real_index == nature_up_index else (0,255,255)
        draw_text(f"{m}", 300, y, color)
    draw_text_center(f"↑↓: 이동 | Enter: 완료", HEIGHT - 40, (180,180,180))

def draw_move_select():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 기술 선택", 40)
    total_pages = (len(available_moves) - 1) // moves_per_page + 1
    start = move_page * moves_per_page
    end = start + moves_per_page
    visible_moves = available_moves[start:end]
    for i, m in enumerate(visible_moves):
        y = 120 + i * 40
        real_index = start + i
        color = (255,255,0) if real_index == move_index else (200,200,200)
        draw_text(f"{m}", 300, y, color)
    draw_text("기술 슬롯:", 650, 120)
    for i in range(4):
        move_name = selected_moves[i] if selected_moves[i] else "-"
        draw_text(f"{i+1}. {move_name}", 650, 160 + i * 40, (255,255,255))
    draw_text_center(f"←→: 페이지 | ↑↓: 이동 | 1~4: 슬롯 지정 | Enter: 완료", HEIGHT - 40, (180,180,180))
    draw_text_center(f"Page {move_page+1}/{total_pages}", HEIGHT - 80, (180,180,180))

def draw_ability_select():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 특성 선택", 40)
    for i, m in enumerate(available_ability):
        y = 120 + i * 40
        real_index=i
        color = (255,255,0) if real_index == ability_index else (200,200,200)
        draw_text(f"{m}", 300, y, color)
    draw_text_center(f"↑↓: 이동 | Enter: 완료", HEIGHT - 40, (180,180,180))

def draw_item_select():
    screen.fill((10, 40, 60))
    draw_text_center(f"{selected_pokemon['name']}의 도구 선택", 40)
    total_pages = (len(available_items) - 1) // items_per_page + 1
    start = item_page * items_per_page
    end = start + items_per_page
    visible_items = available_items[start:end]
    for i, m in enumerate(visible_items):
        y = 120 + i * 40
        real_index = start + i
        color = (255,255,0) if real_index == item_index else (200,200,200)
        draw_text(f"{m}", 300, y, color)
    draw_text_center(f"←→: 페이지 | ↑↓: 이동 | 1~4: 슬롯 지정 | Enter: 완료", HEIGHT - 40, (180,180,180))
    draw_text_center(f"Page {item_page+1}/{total_pages}", HEIGHT - 80, (180,180,180))

def draw_team_preview():
    screen.fill((30, 40, 60))
    draw_text_center("⚔️ 팀 미리보기 ⚔️", 60)
    draw_text("1P 팀:", 200, 150, (255,255,0))
    for i, p in enumerate(team_1):
        draw_text(f"{p['name']}", 220, 200 + i*40, (255,255,255))
    draw_text("2P 팀:", 600, 150, (0,255,255))
    for i, p in enumerate(team_2):
        draw_text(f"{p['name']}", 620, 200 + i*40, (255,255,255))
    draw_text_center("Enter: 출전 포켓몬 선택으로 이동", HEIGHT-60, (180,180,180))

def draw_battle_select(team, player):
    screen.fill((30, 50, 70))
    draw_text_center(f"{player} 출전 포켓몬 선택 (스페이스 선택, Enter 확정)", 60)
    for i, p in enumerate(team):
        y = 150 + i*50
        if i == selected_index and i in selected_for_battle:
            color = (150,255,150)
        elif i == selected_index:
            color = (255,255,0)
        elif i in selected_for_battle:
            color = (0,255,0)
        else:
            color = (255,255,255)
        draw_text(f"{i+1}. {p['name']}", 400, y, color)
    draw_text_center(f"{len(selected_for_battle)}/3 선택됨", HEIGHT-100, (180,180,180))
    draw_text_center("↑↓: 이동 | 스페이스: 선택/해제 | Enter: 확정", HEIGHT-60, (180,180,180))

def draw_battle_ready():
    screen.fill((0, 0, 30))
    draw_text_center("⚔️ 1P vs 2P ⚔️", HEIGHT//2 - 50, (255,255,0))
    draw_text_center("전투 준비 완료!", HEIGHT//2 + 20)
    draw_text_center("Enter로 전투 시작", HEIGHT//2 + 80, (200,200,200))

def another_effect(attacker, defender, move_data, hit):
    if defender.get('ability')=='황금몸':
        print(f"{defender['name']} - 황금몸")
        print(defender)
        return defender
    if not move_data.get("probability") == "0%" and hit and not defender['ability'] == '인분':
        ran = int(move_data['probability'][:-1]) * (2 if attacker['ability'] == '하늘의은총' else 1)
    else:
        return defender
    if int(move_data["eAup"]) and random.random() < ran / 100 and not (
            attacker['ability'] == '우격다짐' and int(move_data['eAup']) < 0):
        defender["rank"][0] = int(numpy.median([-6, 6, defender["rank"][0] + int(move_data["eAup"])]))
        if defender["rank"][0] == 6:
            print(f"하지만 {defender['name']}의 공격은 더이상 오르지 않는다!")
        elif defender["rank"][0] == -6:
            print(f"하지만 {defender['name']}의 공격은 더이상 떨어지지 않는다!")
        elif int(move_data["eAup"]) == 1:
            print(f"{defender['name']}의 공격이 올라갔다!")
        elif int(move_data['eAup']) == 2:
            print(f"{defender['name']}의 공격이 크게 올라갔다!")
        elif int(move_data['eAup']) == 3:
            print(f"{defender['name']}의 공격이 매우 크게 올라갔다!")
        elif int(move_data["eAup"]) == -1:
            print(f"{defender['name']}의 공격이 떨어졌다!")
        elif int(move_data['eAup']) == -2:
            print(f"{defender['name']}의 공격이 크게 떨어졌다!")
        elif int(move_data['eAup']) == -3:
            print(f"{defender['name']}의 공격이 매우 크게 떨어졌다!")
    if int(move_data["eBup"]) and random.random() < ran / 100 and not (
            attacker['ability'] == '우격다짐' and int(move_data['eBup']) < 0):
        defender["rank"][1] = int(numpy.median([-6, 6, defender["rank"][1] + int(move_data["eBup"])]))
        if defender["rank"][1] == 6:
            print(f"하지만 {defender['name']}의 방어는 더이상 오르지 않는다!")
        elif defender["rank"][1] == -6:
            print(f"하지만 {defender['name']}의 방어는 더이상 떨어지지 않는다!")
        elif int(move_data["eBup"]) == 1:
            print(f"{defender['name']}의 방어가 올라갔다!")
        elif int(move_data['eBup']) == 2:
            print(f"{defender['name']}의 방어가 크게 올라갔다!")
        elif int(move_data['eBup']) == 3:
            print(f"{defender['name']}의 방어가 매우 크게 올라갔다!")
        elif int(move_data["eBup"]) == -1:
            print(f"{defender['name']}의 방어가 떨어졌다!")
        elif int(move_data['eBup']) == -2:
            print(f"{defender['name']}의 방어가 크게 떨어졌다!")
        elif int(move_data['eBup']) == -3:
            print(f"{defender['name']}의 방어가 매우 크게 떨어졌다!")
    if int(move_data["eCup"]) and random.random() < ran / 100 and not (
            attacker['ability'] == '우격다짐' and int(move_data['eCup']) < 0):
        defender["rank"][2] = int(numpy.median([-6, 6, defender["rank"][2] + int(move_data["eCup"])]))
        if defender["rank"][2] == 6:
            print(f"하지만 {defender['name']}의 특수공격은 더이상 오르지 않는다!")
        elif defender["rank"][2] == -6:
            print(f"하지만 {defender['name']}의 특수공격은 더이상 떨어지지 않는다!")
        elif int(move_data["eCup"]) == 1:
            print(f"{defender['name']}의 특수공격이 올라갔다!")
        elif int(move_data['eCup']) == 2:
            print(f"{defender['name']}의 특수공격이 크게 올라갔다!")
        elif int(move_data['eCup']) == 3:
            print(f"{defender['name']}의 특수공격이 매우 크게 올라갔다!")
        elif int(move_data["eCup"]) == -1:
            print(f"{defender['name']}의 특수공격이 떨어졌다!")
        elif int(move_data['eCup']) == -2:
            print(f"{defender['name']}의 특수공격이 크게 떨어졌다!")
        elif int(move_data['eCup']) == -3:
            print(f"{defender['name']}의 특수공격이 매우 크게 떨어졌다!")
    if int(move_data["eDup"]) and random.random() < ran / 100 and not (
            attacker['ability'] == '우격다짐' and int(move_data['eDup']) < 0):
        defender["rank"][3] = int(numpy.median([-6, 6, defender["rank"][3] + int(move_data["eDup"])]))
        if defender["rank"][3] == 6:
            print(f"하지만 {defender['name']}의 특수방어는 더이상 오르지 않는다!")
        elif defender["rank"][3] == -6:
            print(f"하지만 {defender['name']}의 특수방어는 더이상 떨어지지 않는다!")
        elif int(move_data["eDup"]) == 1:
            print(f"{defender['name']}의 특수방어가 올라갔다!")
        elif int(move_data['eDup']) == 2:
            print(f"{defender['name']}의 특수방어가 크게 올라갔다!")
        elif int(move_data['eDup']) == 3:
            print(f"{defender['name']}의 특수방어가 매우 크게 올라갔다!")
        elif int(move_data["eDup"]) == -1:
            print(f"{defender['name']}의 특수방어가 떨어졌다!")
        elif int(move_data['eDup']) == -2:
            print(f"{defender['name']}의 특수방어가 크게 떨어졌다!")
        elif int(move_data['eDup']) == -3:
            print(f"{defender['name']}의 특수방어가 매우 크게 떨어졌다!")
    if int(move_data["eSup"]) and random.random() < ran / 100 and not (
            attacker['ability'] == '우격다짐' and int(move_data['eEup']) < 0):
        defender["rank"][4] = int(numpy.median([-6, 6, defender["rank"][4] + int(move_data["eSup"])]))
        if defender["rank"][4] == 6:
            print(f"하지만 {defender['name']}의 스피드는 더이상 오르지 않는다!")
        elif defender["rank"][4] == -6:
            print(f"하지만 {defender['name']}의 스피드는 더이상 떨어지지 않는다!")
        elif int(move_data["eSup"]) == 1:
            print(f"{defender['name']}의 스피드가 올라갔다!")
        elif int(move_data['eSup']) == 2:
            print(f"{defender['name']}의 스피드가 크게 올라갔다!")
        elif int(move_data['eSup']) == 3:
            print(f"{defender['name']}의 스피드가 매우 크게 올라갔다!")
        elif int(move_data["eSup"]) == -1:
            print(f"{defender['name']}의 스피드가 떨어졌다!")
        elif int(move_data['eSup']) == -2:
            print(f"{defender['name']}의 스피드가 크게 떨어졌다!")
        elif int(move_data['eSup']) == -3:
            print(f"{defender['name']}의 스피드가 매우 크게 떨어졌다!")
    if field=="Mist" and not(('비행' in defender["type"] or defender['ability']=='부유') and not gravity):
        return defender
    if (int(move_data["Flinch"]) and random.random() < ran / 100 and not defender["ability"] == "정신력"
            and not defender["ability"] == "인분" and not attacker['ability'] == '우격다짐'):
        defender['Flinch'] = 1
    if (int(move_data["Confusion"]) and random.random() < ran / 100 and not defender["ability"] == "마이페이스"
            and not attacker['ability'] == '우격다짐'):
        defender['Confusion'] = 1
    if (int(move_data["Binding"]) and random.random() < ran / 100
            and not attacker['ability'] == '우격다짐'):
        defender['Binding'] = 1
    if (int(move_data["Freeze"]) and random.random() < ran / 100 and defender["status"] == None
            and not '얼음' in defender['type'] and not attacker['ability'] == '우격다짐'):
        defender['status'] = "Freeze"
        print(f"{defender['name']}은(는) 얼어붙었다!")
    if (int(move_data['Sleep']) and random.random() < ran / 100 and defender["status"] == None
            and not defender["ability"] == "의기양양" and not defender["ability"] == "불면"
            and not attacker['ability'] == '우격다짐' and not(field=="Electric" and not(('비행' in defender["type"] or defender['ability']=='부유') and not gravity))):
        defender['status'] = "Sleep"
        print(f"{defender['name']}은(는) 잠들어 버렸다!")
    if (int(move_data['Paralysis']) and random.random() < ran / 100 and defender["status"] == None
            and not defender['ability'] == '유연' and not '전기' in defender['type']
            and not attacker['ability'] == '우격다짐'):
        defender['status'] = "Paralysis"
        print(f"{defender['name']}은(는) 마비되어 기술이 나오기 어려워졌다!")
    if (int(move_data["Burn"]) and random.random() < ran / 100 and defender["status"] == None
            and not defender['ability'] == '수의베일' and not defender['ability'] == '수포'
            and not defender['ability'] == '열교환' and not "불꽃" in defender['type']
            and not attacker['ability'] == '우격다짐'):
        defender['status'] = "Burn"
        print(f"{defender['name']}은(는) 화상을 입었다!")
    if (int(move_data["Poison"]) and random.random() < ran / 100 and defender["status"] == None
            and not defender['ability'] == '면역' and not "독" in defender['type']
            and not "강철" in defender['type'] and not attacker['ability'] == '우격다짐'):
        defender['status'] = "Poison"
        print(f"{defender['name']}의 몸에 독이 퍼졌다!")
    if (int(move_data["SPoison"]) and random.random() < ran / 100 and defender["status"] == None and not defender[
                                                                                                        'ability'] == '면역'
            and not "독" in defender['type'] and not "강철" in defender['type']
            and not attacker['ability'] == '우격다짐'):
        defender['status'] = "SPoison"
        print(f"{defender['name']}의 몸에 독이 퍼졌다!")
    return defender

def rebound_calculate(attacker, dmg, move_data, hit):
    if move_data['name']=="발버둥":
        rebounded_dmg=attacker['max_status'][0]//4
    elif move_data['rebound'] == '0%' or attacker['ability'] == '돌머리' or attacker['ability'] == '매직가드' or not hit:
        rebounded_dmg=0
    else:
        rebounded_dmg= dmg * int(move_data['rebound'][:-1]) / 100
        if not move_data['rebound'] == '0%' and rebounded_dmg>0:
            print(f"{attacker['name']}은(는) 반동으로 데미지를 입었다!")
        elif not move_data['rebound'] == '0%' and rebounded_dmg<0:
            print(f"{attacker['name']}은(는) 체력을 회복했다!")
    return int(rebounded_dmg)

def side_effect(attacker, move_data, hit):
    if not hit:
        return attacker['rank']
    if int(move_data['Aup']) and not (attacker['ability'] == '우격다짐' and int(move_data['Aup']) > 0):
        attacker['rank'][0] = int(numpy.median([attacker['rank'][0] + int(move_data['Aup']), -6, 6]))
        if attacker["rank"][0] == 6:
            print(f"하지만 {attacker['name']}의 공격은 더이상 오르지 않는다!")
        elif attacker["rank"][0] == -6:
            print(f"하지만 {attacker['name']}의 공격은 더이상 떨어지지 않는다!")
        elif int(move_data["Aup"]) == 1:
            print(f"{attacker['name']}의 공격이 올라갔다!")
        elif int(move_data['Aup']) == 2:
            print(f"{attacker['name']}의 공격이 크게 올라갔다!")
        elif int(move_data['Aup']) == 3:
            print(f"{attacker['name']}의 공격이 매우 크게 올라갔다!")
        elif int(move_data["Aup"]) == -1:
            print(f"{attacker['name']}의 공격이 떨어졌다!")
        elif int(move_data['Aup']) == -2:
            print(f"{attacker['name']}의 공격이 크게 떨어졌다!")
        elif int(move_data['Aup']) == -3:
            print(f"{attacker['name']}의 공격이 매우 크게 떨어졌다!")
    if int(move_data['Bup']) and not (attacker['ability'] == '우격다짐' and int(move_data['Bup']) > 0):
        attacker['rank'][1] = int(numpy.median([attacker['rank'][1] + int(move_data['Bup']), -6, 6]))
        if attacker["rank"][1] == 6:
            print(f"하지만 {attacker['name']}의 방어는 더이상 오르지 않는다!")
        elif attacker["rank"][1] == -6:
            print(f"하지만 {attacker['name']}의 방어는 더이상 떨어지지 않는다!")
        elif int(move_data["Bup"]) == 1:
            print(f"{attacker['name']}의 방어가 올라갔다!")
        elif int(move_data['Bup']) == 2:
            print(f"{attacker['name']}의 방어가 크게 올라갔다!")
        elif int(move_data['Bup']) == 3:
            print(f"{attacker['name']}의 방어가 매우 크게 올라갔다!")
        elif int(move_data["Bup"]) == -1:
            print(f"{attacker['name']}의 방어가 떨어졌다!")
        elif int(move_data['Bup']) == -2:
            print(f"{attacker['name']}의 방어가 크게 떨어졌다!")
        elif int(move_data['Bup']) == -3:
            print(f"{attacker['name']}의 방어가 매우 크게 떨어졌다!")
    if int(move_data['Cup']) and not (attacker['ability'] == '우격다짐' and int(move_data['Cup']) > 0):
        attacker['rank'][2] = int(numpy.median([attacker['rank'][2] + int(move_data['Cup']), -6, 6]))
        if attacker["rank"][2] == 6:
            print(f"하지만 {attacker['name']}의 특수공격은 더이상 오르지 않는다!")
        elif attacker["rank"][2] == -6:
            print(f"하지만 {attacker['name']}의 특수공격은 더이상 떨어지지 않는다!")
        elif int(move_data["Cup"]) == 1:
            print(f"{attacker['name']}의 특수공격이 올라갔다!")
        elif int(move_data['Cup']) == 2:
            print(f"{attacker['name']}의 특수공격이 크게 올라갔다!")
        elif int(move_data['Cup']) == 3:
            print(f"{attacker['name']}의 특수공격이 매우 크게 올라갔다!")
        elif int(move_data["Cup"]) == -1:
            print(f"{attacker['name']}의 특수공격이 떨어졌다!")
        elif int(move_data['Cup']) == -2:
            print(f"{attacker['name']}의 특수공격이 크게 떨어졌다!")
        elif int(move_data['Cup']) == -3:
            print(f"{attacker['name']}의 특수공격이 매우 크게 떨어졌다!")
    if int(move_data['Dup']) and not (attacker['ability'] == '우격다짐' and int(move_data['Dup']) > 0):
        attacker['rank'][3] = int(numpy.median([attacker['rank'][3] + int(move_data['Dup']), -6, 6]))
        if attacker["rank"][3] == 6:
            print(f"하지만 {attacker['name']}의 특수방어는 더이상 오르지 않는다!")
        elif attacker["rank"][3] == -6:
            print(f"하지만 {attacker['name']}의 특수방어는 더이상 떨어지지 않는다!")
        elif int(move_data["Dup"]) == 1:
            print(f"{attacker['name']}의 특수방어가 올라갔다!")
        elif int(move_data['Dup']) == 2:
            print(f"{attacker['name']}의 특수방어가 크게 올라갔다!")
        elif int(move_data['Dup']) == 3:
            print(f"{attacker['name']}의 특수방어가 매우 크게 올라갔다!")
        elif int(move_data["Dup"]) == -1:
            print(f"{attacker['name']}의 특수방어가 떨어졌다!")
        elif int(move_data['Dup']) == -2:
            print(f"{attacker['name']}의 특수방어가 크게 떨어졌다!")
        elif int(move_data['Dup']) == -3:
            print(f"{attacker['name']}의 특수방어가 매우 크게 떨어졌다!")
    if int(move_data['Sup']) and not (attacker['ability'] == '우격다짐' and int(move_data['Sup']) > 0):
        attacker['rank'][4] = int(numpy.median([attacker['rank'][4] + int(move_data['Sup']), -6, 6]))
        if attacker["rank"][4] == 6:
            print(f"하지만 {attacker['name']}의 스피드는 더이상 오르지 않는다!")
        elif attacker["rank"][4] == -6:
            print(f"하지만 {attacker['name']}의 스피드는 더이상 떨어지지 않는다!")
        elif int(move_data["Sup"]) == 1:
            print(f"{attacker['name']}의 스피드가 올라갔다!")
        elif int(move_data['Sup']) == 2:
            print(f"{attacker['name']}의 스피드가 크게 올라갔다!")
        elif int(move_data['Sup']) == 3:
            print(f"{attacker['name']}의 스피드가 매우 크게 올라갔다!")
        elif int(move_data["Sup"]) == -1:
            print(f"{attacker['name']}의 스피드가 떨어졌다!")
        elif int(move_data['Sup']) == -2:
            print(f"{attacker['name']}의 스피드가 크게 떨어졌다!")
        elif int(move_data['Sup']) == -3:
            print(f"{attacker['name']}의 스피드가 매우 크게 떨어졌다!")
    return attacker['rank']

def draw_battle_screen(p1_pokemon, p2_pokemon, p1_hp, p2_hp):
    screen.fill((20, 20, 40))
    draw_text_center("⚔️ BATTLE START ⚔️", 40, (255, 255, 255))

    draw_text(f"1P: {p1_pokemon['name']}", 100, 150, (255, 255, 0))
    pygame.draw.rect(screen, (255, 0, 0), (100, 180, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (100, 180, int(200 * p1_hp / p1_pokemon['max_status'][0]), 20))
    draw_text(f"HP: {p1_hp}/{p1_pokemon['max_status'][0]}", 100, 210, (255, 255, 255))

    draw_text(f"2P: {p2_pokemon['name']}", 500, 50, (0, 200, 255))
    pygame.draw.rect(screen, (255, 0, 0), (500, 80, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (500, 80, int(200 * p2_hp / p2_pokemon['max_status'][0]), 20))
    draw_text(f"HP: {p2_hp}/{p2_pokemon['max_status'][0]}", 500, 110, (255, 255, 255))

    pygame.display.flip()

def type_multiplier(move_type, defender_type):
    multiplier = 1
    for t in defender_type:
        multiplier *= type_chart.get(move_type, {}).get(t, 1.0)
    return multiplier

def qoWkd_type_multiplier(move_type,defender_type):
    multiplier = 1
    for t in defender_type:
        multiplier *= qoWkd_type_chart.get(move_type, {}).get(t, 1.0)
    return multiplier

def calculate_damage(attacker, defender, move_data, weather=None, reflect=False, l_screen=False, field=None,gravity=False,wonder_room=False):
    """
    :param attacker:
    :param defender:
    :param move_data:
    :param weather:
    :param reflect:
    :param l_screen:
    :param field:
    :param gravity:
    :param wonder_room:
    :return: tuple(damage, hit, type_mult, is_crit, par_flag, flinch_flag,except_flag)
    """
    par_flag,flinch_flag,except_flag=0,0,0
    if defender.get('ability')=='저수' and move_data['type']=='물':
        print(f"{defender['name']} - 저수")
        print(f"{defender['name']}은(는) 체력을 회복했다!")
        hit=0
        except_flag=1
        return 0-defender['max_status']//4, hit, 0, 0, par_flag, flinch_flag,except_flag
    if (random.random() < int(move_data["accuracy"]) / 100 * (
            (3 + max(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]])))) / (
            3 - min(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]]))))) or
            int(move_data['accuracy'])==-1):
        hit = 1
    else:
        hit = 0
        return 0, hit, 0, 0, par_flag, flinch_flag,except_flag
    if attacker["status"] == "Paralysis" and random.random() < 25:
        hit = 0
        par_flag = 1
        return 0, hit, 0, 0, par_flag, flinch_flag,except_flag
    if attacker['Flinch']:
        hit = 0
        print(f"{attacker['name']}은(는) 풀이 죽어 기술을 쓸 수 없다!")
        flinch_flag = 1
        return 0, hit, 0, 0, par_flag,flinch_flag,except_flag
    if move_data['name']=='속이기' and not attacker['turn']==1:
        hit = 0
        print(f"{attacker['name']}의 {move_name}!")
        print('하지만 실패했다!')
        except_flag = 1
        return 0, hit, 0, 0, par_flag,flinch_flag,except_flag
    if int(move_data['priority']) and field=='Psyco' and not(('비행' in defender["type"] or defender['ability']=='부유') and not gravity):
        hit = 0
        except_flag=1
        print(f"{attacker['name']}의 {move_name}!")
        print(f"사이코필드가 {defender['name']}을(를) 지켜냈다!")
        return 0, hit, 0, 0, par_flag,flinch_flag,except_flag
    if move_data.get("fixed_damage"):
        return move_data["fixed_damage"], 1,0,0,0,0,except_flag
    power = int(move_data["power"])
    move_type = move_data["type"]
    category = move_data["category"]
    atk_index = 1 if category == "물리" else 3
    atk_stat = attacker["current_status"][atk_index]
    if wonder_room:
        def_index= 2 if category == '특수' else 4
    else:
        def_index = 2 if category == '물리' else 4
    def_stat = defender["current_status"][def_index]

    power_mod = 1.0
    if attacker.get("ability") == "이판사판" and not move_data.get("rebound") == 0: power_mod *= 1.2
    if attacker.get("ability") == "심록" and attacker.get("current_status")[0] * 3 <= attacker.get("max_status")[
        0] and move_data.get("type") == "풀": power_mod *= 1.5
    if attacker.get("ability") == "맹화" and attacker.get("current_status")[0] * 3 <= attacker.get("max_status")[
        0] and move_data.get("type") == "불꽃": power_mod *= 1.5
    if attacker.get("ability") == "급류" and attacker.get("current_status")[0] * 3 <= attacker.get("max_status")[
        0] and move_data.get("type") == "물": power_mod *= 1.5
    if attacker.get("ability") == "벌레의알림" and attacker.get("current_status")[0] * 3 <= attacker.get("max_status")[
        0] and move_data.get("type") == "벌레": power_mod *= 1.5
    if attacker.get("ability") == "테크니션" and power <= 60: power_mod *= 1.5
    if attacker.get("ability") == "철주먹" and "펀치" in move_data["property"]: power_mod *= 1.2
    if attacker.get("ability") == "우격다짐" and (
        not int(move_data["probability"]) == 0 or int(move_data["Aup"]) > 0 or
        int(move_data["Bup"]) > 0 or int(move_data["Cup"]) > 0 or
        int(move_data["Dup"]) > 0 or int(move_data["Sup"]) > 0 or
        int(move_data["eHup"]) < 0 or int( move_data["eAup"]) < 0 or
        int(move_data["eBup"]) < 0 or int(move_data["eCup"]) < 0 or
        int(move_data["eDup"]) < 0 or int(move_data["eSup"]) < 0): power_mod *= 1.3
    if attacker.get("ability") == "단단한발톱" and "접촉" in move_data["property"]: power_mod *= 1.3
    if attacker.get("ability") == "펑크록" and "소리" in move_data["property"]: power_mod *= 1.3
    if attacker.get("ability") == "메가런처" and "파동" in move_data["property"]: power_mod *= 1.5
    if attacker.get("ability") == "예리함" and "베기" in move_data["property"]: power_mod *= 1.5
    if attacker.get("ability") == "옹골찬턱" and "뮬기" in move_data["property"]: power_mod *= 1.5
    if attacker.get("ability") == "의욕": power_mod *= 1.5
    if attacker.get("ability") == "강철술사" and move_type == "강철": power_mod *= 1.5
    if attacker.get("ability") == "순수한힘" and category == "물리": power_mod *= 2.0
    if attacker.get("ability") == "천하장사" and category == "물리": power_mod *= 2.0
    if attacker.get('ability')=='스카이스킨' and move_type == '노말':power_mod *= 1.2; move_type='비행'
    if attacker.get('ability')=='페어리스킨' and move_type == '노말':power_mod *= 1.2; move_type='페어리'
    if attacker.get('ability')=='프리즈스킨' and move_type == '노말':power_mod *= 1.2; move_type='얼음'
    if attacker.get('ability')=='일렉트릭스킨' and move_type == '노말':power_mod *= 1.2; move_type='전기'
    if attacker.get('ability')=='노말스킨':power_mod *= 1.2;move_type='노말'
    if move_data.get('name')=='객기' and not attacker.get('status') == None: power_mod *= 2.0

    atk_mod = 1.0
    def_mod = 1.0
    atk_mod *= (2 + max(0, attacker["rank"][atk_index - 1])) / (2 - min(0, attacker["rank"][atk_index - 1]))
    if (attacker.get('ability') == '진홍빛고동') and weather == 'Sun' and atk_index==1: atk_mod*=1.3
    if (attacker.get('ability') == '하드론엔진') and field=='Electric' and atk_index==3: atk_mod*=1.3
    if attacker.get('ability')=='근성' and not attacker.get('status')==None: atk_mod*=1.5
    def_mod *= (2 + max(0, defender["rank"][def_index - 1])) / (2 - min(0, defender["rank"][def_index - 1]))
    atk_final = int(atk_stat * atk_mod)
    def_final = int(def_stat * def_mod)

    if attacker["status"] == "Burn" and category == "물리":
        power_mod *= 0.5
    if weather == "Sun" and move_type == "불꽃": power_mod *= 1.5
    if weather == "Rain" and move_type == "불꽃": power_mod *= 0.5
    if weather == "VerySun" and move_type == "불꽃": power_mod *= 1.5
    if weather == "VerySun" and move_type == "물": power_mod *= 0
    if weather == "Sun" and move_type == "물": power_mod *= 0.5
    if weather == "Rain" and move_type == "물": power_mod *= 1.5
    if weather == "VeryRain" and move_type == "물": power_mod *= 1.5
    if weather == "VeryRain" and move_type == "불꽃": power_mod *= 0
    if reflect and category == "물리": power_mod *= 0.5
    if l_screen and category == "특수": power_mod *= 0.5
    if field == 'Grass' and move_type=='풀' and not(("비행" in attacker['type'] or attacker['ability']=='부유')and not gravity): power_mod *= 1.3
    if field == 'Psyco' and move_type=='에스퍼' and not(("비행" in attacker['type'] or attacker['ability']=='부유')and not gravity): power_mod *= 1.3
    if field == 'Mist' and move_type=='드래곤' and not(("비행" in attacker['type'] or attacker['ability']=='부유')and not gravity): power_mod *= 0.5
    if field == 'Electric' and move_type=='전기' and not(("비행" in attacker['type'] or attacker['ability']=='부유')and not gravity): power_mod *= 1.3
    critical = 1.0
    if defender.get("ability") == "조가비갑옷":
        is_crit = 0
    elif attacker.get("rank")[7]+int(move_data['critical']) == 0:
        if random.randint(1, 24) == 1:
            is_crit = 1
        else:
            is_crit = 0
    elif attacker.get("rank")[7]+int(move_data['critical']) == 1:
        if random.randint(1, 8) == 1:
            is_crit = 1
        else:
            is_crit = 0
    elif attacker.get("rank")[7]+int(move_data['critical']) == 2:
        if random.randint(1, 2) == 1:
            is_crit = 1
        else:
            is_crit = 0
    else:
        is_crit = 1
    if is_crit:
        critical = 2.25 if attacker.get("ability") == "스나이퍼" else 1.5

    rand_choices = [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    weights = [7.69, 5.13, 7.69, 5.13, 7.69, 7.69, 5.13, 7.69, 5.13, 7.69, 5.13, 7.69, 5.13, 7.69, 5.13, 2.56]
    rand_val = random.choices(rand_choices, weights=weights, k=1)[0]

    if move_type in attacker["type"]:
        if attacker.get("ability") == "적응력":
            stab = 2.0
        else:
            stab = 1.5
    else:
        stab = 1.0
    if (move_type=='노말' or move_type=='격투') and attacker['ability']=='배짱':
        type_mult=qoWkd_type_multiplier(move_type,defender['type'])
    else:
        type_mult = type_multiplier(move_type, defender["type"])
    if attacker.get("ability") == "불가사의부적" and type_mult < 1: type_mult *= 0
    if attacker.get("item") == "달인의띠" and type_mult > 1: power_mod *= 1.2
    if defender.get("ability") == '부유' and move_type == "땅": type_mult *= 0

    if attacker.get("ability") == "방음" and "소리" in move_data.get("property").split(","): power_mod *= 0
    if attacker.get("ability") == "방진" and "가루" in move_data.get("property").split(","): power_mod *= 0
    if attacker.get("ability") == "방음" and "소리" in move_data.get("property").split(","): power_mod *= 0
    mod2 = 1.0
    if attacker.get("item") == "생명의구슬": mod2 *= 1.3
    if attacker.get('item') == '실크스카프' and move_data['type']=='노말': mod2 *= 1.2
    if attacker.get('item') == '목탄' and move_data['type'] == '불꽃': mod2 *= 1.2
    if attacker.get('item') == '신비의물방울' and move_data['type'] == '물': mod2 *= 1.2
    if attacker.get('item') == '기적의씨' and move_data['type'] == '풀': mod2 *= 1.2
    if attacker.get('item') == '자석' and move_data['type'] == '전기': mod2 *= 1.2
    if attacker.get('item') == '녹지않는얼음' and move_data['type'] == '얼음': mod2 *= 1.2
    if attacker.get('item') == '검은띠' and move_data['type'] == '격투': mod2 *= 1.2
    if attacker.get('item') == '독바늘' and move_data['type'] == '독': mod2 *= 1.2
    if attacker.get('item') == '부드러운모래' and move_data['type'] == '땅': mod2 *= 1.2
    if attacker.get('item') == '예리한부리' and move_data['type'] == '비행': mod2 *= 1.2
    if attacker.get('item') == '휘어진스푼' and move_data['type'] == '에스퍼': mod2 *= 1.2
    if attacker.get('item') == '은빛가루' and move_data['type'] == '벌레': mod2 *= 1.2
    if attacker.get('item') == '딱딱한돌' and move_data['type'] == '바위': mod2 *= 1.2
    if attacker.get('item') == '저주의부적' and move_data['type'] == '고스트': mod2 *= 1.2
    if attacker.get('item') == '용의이빨' and move_data['type'] == '드래곤': mod2 *= 1.2
    if attacker.get('item') == '검은안경' and move_data['type'] == '악': mod2 *= 1.2
    if attacker.get('item') == '금속코트' and move_data['type'] == '강철': mod2 *= 1.2
    if attacker.get('item') == '요정의깃털' and move_data['type'] == '페어리': mod2 *= 1.2
    if attacker.get('item')[-2:]=='주얼' and attacker.get('item')[:-2]==move_data['type']: mod2 *= 1.3
    mod3 = 1.0
    if defender.get("ability") == "필터" and type_mult > 1: mod3 *= 0.75
    if defender.get("ability") == '하드록' and type_mult > 1: mod3 *= 0.75
    if attacker.get("item") == "달인의띠" and type_mult > 1: mod3 *= 1.2
    if attacker.get("ability") == "색안경" and type_mult < 1: mod3 *= 2
    modified_power = int(power * power_mod * mod2 * mod3 * type_mult * stab)
    base_damage = ((22 * modified_power * atk_final // (def_final * 50 + 2)) * (rand_val / 100)) * critical
    if defender.get('ability')=='멀티스케일' and defender.get('current_status')[0]==defender.get('max_status')[0]:base_damage//=2
    damage = math.floor(base_damage)

    if type_mult > 0 and damage < 1:
        damage = 1

    return damage, hit, type_mult, is_crit, par_flag, flinch_flag,except_flag

def choose_action(player_num):
    choosing=True
    selected_action = None
    while choosing:
        screen.fill((0, 0, 0))
        draw_text_center(f"{player_num}P: 행동을 선택하세요 1 : 포켓몬  2 : 기술",200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2]:
                    if int(event.unicode)==1:
                        selected_action = "교체"
                        choosing = False
                    else:
                        selected_action = "기술"
                        choosing = False
    return selected_action

def choose_pokemon(player_num, team, current_pokemon_id):
    choosing = True
    chosen_pokemon = None
    idx=None
    while choosing:
        screen.fill((0, 0, 0))
        draw_text_center(f"{player_num}P: 무슨 포켓몬으로 교체하시겠습니까? (1~3)", 200)
        for i, pokemon in enumerate(team):
            draw_text_center(f"{i + 1}. {pokemon['name']}", 260 + i * 40,(255,255,255) if not pokemon['current_status'][0]==0 else (255,0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    idx = int(event.unicode) - 1
                    if not idx == current_pokemon_id and not team[idx]['current_status'][0]==0:
                        chosen_pokemon = team[idx]
                        choosing = False
                        ca=0
                    else:
                        choosing=False
                        ca=1
                elif event.key == pygame.K_ESCAPE:
                    choosing=False
                    ca=1
    return chosen_pokemon, idx,ca

def choose_move(player_num, pokemon):
    choosing = True
    selected_move = None
    idx=None
    while choosing:
        screen.fill((0, 0, 0))
        draw_text_center(f"{player_num}P: {pokemon['name']}의 기술을 선택하세요 (1~4)", 200)
        for i, mv in enumerate(pokemon["moves"]):
            draw_text_center(f"{i + 1}. {mv}  PP:{pokemon['PP'][i]}", 260 + i * 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4] and pokemon["moves"][int(event.unicode)-1] and pokemon["PP"][int(event.unicode)-1]:
                    idx = int(event.unicode) - 1
                    if 0 <= idx < len(pokemon["moves"]):
                        selected_move = pokemon["moves"][idx]
                        choosing = False
                        ca=0
                if event.type == pygame.K_ESCAPE:
                    choosing=False
                    ca=1
    return selected_move,idx,ca

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "select_pokemon" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                page = (page + 1) % ((len(pokemon_data) - 1) // pokemon_per_page + 1)
            elif event.key == pygame.K_LEFT:
                page = (page - 1) % ((len(pokemon_data) - 1) // pokemon_per_page + 1)
            elif event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % pokemon_per_page
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % pokemon_per_page
            elif event.key == pygame.K_RETURN:
                idx = page * pokemon_per_page + selected_index
                if idx < len(pokemon_data):
                    selected_pokemon = pokemon_data[idx]
                    iv_points = [31, 31, 31, 31, 31, 31]
                    iv_index = 0
                    input_buffer = ""
                    state = "iv_setting"

        elif state == "iv_setting" and event.type == pygame.KEYDOWN:
            total = sum(iv_points)
            if event.key == pygame.K_DOWN:
                iv_index = (iv_index + 1) % 6
            elif event.key == pygame.K_UP:
                iv_index = (iv_index - 1) % 6
            elif event.key == pygame.K_RIGHT:
                if iv_points[iv_index] < 31:
                    iv_points[iv_index] = min(31, iv_points[iv_index] + 10)
            elif event.key == pygame.K_LEFT:
                iv_points[iv_index] = max(0, iv_points[iv_index] - 10)
            elif event.key == pygame.K_RETURN:
                if input_buffer:
                    try:
                        val = int(input_buffer)
                        if 0 <= val <= 31:
                            iv_points[iv_index] = val
                    except ValueError:
                        pass
                    input_buffer = ""
                else:
                    ev_points = [0, 0, 0, 0, 0, 0]
                    ev_index = 0
                    input_buffer = ""
                    state = "ev_setting"
            elif event.key == pygame.K_BACKSPACE:
                input_buffer = input_buffer[:-1]
            elif event.key == pygame.K_ESCAPE:
                state = "select_pokemon"
            elif event.unicode.isdigit():
                if len(input_buffer) < 2:
                    input_buffer += event.unicode

        elif state == "ev_setting" and event.type == pygame.KEYDOWN:
            total = sum(ev_points)
            if event.key == pygame.K_DOWN:
                ev_index = (ev_index + 1) % 6
            elif event.key == pygame.K_UP:
                ev_index = (ev_index - 1) % 6
            elif event.key == pygame.K_RETURN:
                if input_buffer:
                    try:
                        val = int(input_buffer)
                        total_without_current = sum(ev_points) - ev_points[ev_index]
                        if 0 <= val <= 252 and total_without_current + val <= max_ev_total:
                            ev_points[ev_index] = val
                    except ValueError:
                        pass
                    input_buffer = ""
                else:
                    nature=[0,0,0,0,0]
                    nature_index = 0
                    state = "nature_up_setting"
            elif event.key == pygame.K_BACKSPACE:
                input_buffer = input_buffer[:-1]
            elif event.key == pygame.K_ESCAPE:
                state="iv_setting"
            elif event.unicode.isdigit():
                if len(input_buffer) < 3:
                    input_buffer += event.unicode

        elif state == "nature_up_setting" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                nature_index = (nature_index + 1) % len(nature_names)
            elif event.key == pygame.K_UP:
                nature_index = (nature_index - 1) % len(nature_names)
            elif event.key == pygame.K_ESCAPE:
                state="ev_setting"
            elif event.key == pygame.K_RETURN:
                nature[nature_index]+=1
                nature_up_index=nature_index
                state="nature_down_setting"

        elif state == "nature_down_setting" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                nature_index = (nature_index + 1) % len(nature_names)
            elif event.key == pygame.K_UP:
                nature_index = (nature_index - 1) % len(nature_names)
            elif event.key == pygame.K_ESCAPE:
                state = "ev_setting"
            elif event.key == pygame.K_RETURN:
                nature[nature_index] -= 1
                move_names = selected_pokemon["moves"].split(",")
                available_moves = [m.strip() for m in move_names if m.strip()]
                selected_moves = [""] * 4
                move_index = 0
                move_page = 0
                selected_moves_PP=[0,0,0,0]
                state = "move_select"

        elif state == "move_select" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                move_index = (move_index + 1) % len(available_moves)
                move_page = move_index // moves_per_page
            elif event.key == pygame.K_UP:
                move_index = (move_index - 1) % len(available_moves)
                move_page = move_index // moves_per_page
            elif event.key == pygame.K_RIGHT:
                move_page = (move_page + 1) % ((len(available_moves) - 1) // moves_per_page + 1)
                move_index = move_page * moves_per_page
            elif event.key == pygame.K_LEFT:
                move_page = (move_page - 1) % ((len(available_moves) - 1) // moves_per_page + 1)
                move_index = move_page * moves_per_page
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                slot = int(event.unicode) - 1
                selected_moves[slot] = available_moves[move_index]
                selected_moves_PP[slot] = int(find_move(selected_moves[slot])["pp"])
            elif event.key == pygame.K_ESCAPE:
                state="ev_setting"
            elif event.key == pygame.K_RETURN and (selected_moves[0] or selected_moves[1] or selected_moves[2] or selected_moves[3]):
                state="item_select"
                selected_item = []
                item_index = 0

        elif state == "item_select" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                item_index = (item_index + 1) % len(available_items)
                item_page = item_index // items_per_page
            elif event.key == pygame.K_UP:
                item_index = (item_index - 1) % len(available_items)
                item_page = item_index // items_per_page
            elif event.key == pygame.K_RIGHT:
                item_page = (item_page + 1) % ((len(available_items) - 1) // items_per_page + 1)
                item_index = item_page * items_per_page
            elif event.key == pygame.K_LEFT:
                item_page = (item_page - 1) % ((len(available_items) - 1) // items_per_page + 1)
                item_index = item_page * items_per_page
            elif event.key == pygame.K_ESCAPE:
                state="move_select"
            elif event.key == pygame.K_RETURN:
                selected_item = available_items[item_index]
                state="ability_select"
                ability_names = selected_pokemon["ability"].split(",")
                available_ability = [m.strip() for m in ability_names if m.strip()]
                selected_ability = []
                ability_index = 0

        elif state == "ability_select" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                ability_index = (ability_index + 1) % len(available_ability)
            elif event.key == pygame.K_UP:
                ability_index = (ability_index - 1) % len(available_ability)
            elif event.key == pygame.K_ESCAPE:
                state="item_select"
            elif event.key == pygame.K_RETURN:
                selected_ability = available_ability[ability_index]
                chosen_data = {
                    "type": [selected_pokemon["type1"]]if selected_pokemon["type2"] == "" else [selected_pokemon["type1"],selected_pokemon["type2"]],
                    "name": selected_pokemon["name"],
                    "ivs": iv_points.copy(),
                    "evs": ev_points.copy(),
                    "moves": selected_moves.copy(),
                    "ability": selected_ability,"item":selected_item,
                    "current_status":[int((int(selected_pokemon["hp"])*2+iv_points[0]+ev_points[0]/4+100)/2+10),
                                      int(int((int(selected_pokemon["attack"])*2+iv_points[1]+ev_points[1]/4)/2+5)*(1.1 if nature[0] == 1 else 0.9 if nature[0] == -1 else 1)),
                                      int(int((int(selected_pokemon["defense"])*2+iv_points[2]+ev_points[2]/4)/2+5)*(1.1 if nature[1] == 1 else 0.9 if nature[1] == -1 else 1)),
                                      int(int((int(selected_pokemon["sp_atk"])*2+iv_points[3]+ev_points[3]/4)/2+5)*(1.1 if nature[2] == 1 else 0.9 if nature[2] == -1 else 1)),
                                      int(int((int(selected_pokemon["sp_def"])*2+iv_points[4]+ev_points[4]/4)/2+5)*(1.1 if nature[3] == 1 else 0.9 if nature[3] == -1 else 1)),
                                      int(int((int(selected_pokemon["speed"])*2+iv_points[5]+ev_points[5]/4)/2+5)*(1.1 if nature[4] == 1 else 0.9 if nature[4] == -1 else 1))],
                    "max_status":[int((int(selected_pokemon["hp"])*2+iv_points[0]+ev_points[0]/4+100)/2+10),
                                      int(int((int(selected_pokemon["attack"])*2+iv_points[1]+ev_points[1]/4)/2+5)*(1.1 if nature[0] == 1 else 0.9 if nature[0] == -1 else 1)),
                                      int(int((int(selected_pokemon["defense"])*2+iv_points[2]+ev_points[2]/4)/2+5)*(1.1 if nature[1] == 1 else 0.9 if nature[1] == -1 else 1)),
                                      int(int((int(selected_pokemon["sp_atk"])*2+iv_points[3]+ev_points[3]/4)/2+5)*(1.1 if nature[2] == 1 else 0.9 if nature[2] == -1 else 1)),
                                      int(int((int(selected_pokemon["sp_def"])*2+iv_points[4]+ev_points[4]/4)/2+5)*(1.1 if nature[3] == 1 else 0.9 if nature[3] == -1 else 1)),
                                      int(int((int(selected_pokemon["speed"])*2+iv_points[5]+ev_points[5]/4)/2+5)*(1.1 if nature[4] == 1 else 0.9 if nature[4] == -1 else 1))],
                    "rank":[0,0,0,0,0,0,0,0],
                    "nature":nature.copy(),
                    "status":None,
                    "Flinch":0,
                    "Confusion":0,
                    "Binding":0,
                    "SPoison_cnt":1,
                    "PP":selected_moves_PP.copy(),
                    "turn":0,"protect":False,
                    "next_move":None
                }
                if current_player == 1:
                    team_1.append(chosen_data)
                    if len(team_1) == 6:
                        current_player = 2
                        page, selected_index = 0, 0
                    state = "select_pokemon"
                else:
                    team_2.append(chosen_data)
                    if len(team_2) == 6:
                        state = "team_preview"
                    else:
                        state = "select_pokemon"

        elif state == "team_preview" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                selected_for_battle = []
                selected_index = 0
                state = "battle_select_1"

        elif state in ["battle_select_1", "battle_select_2"] and event.type == pygame.KEYDOWN:
            team = team_1 if state == "battle_select_1" else team_2
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(team)
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(team)
            elif event.key == pygame.K_SPACE:
                if selected_index in selected_for_battle:
                    selected_for_battle.remove(selected_index)
                elif len(selected_for_battle) < 3:
                    selected_for_battle.append(selected_index)
            elif event.key == pygame.K_RETURN and (len(selected_for_battle)==3):
                chosen = [team[i] for i in selected_for_battle]
                if state == "battle_select_1":
                    battle_team_1 = chosen
                    selected_for_battle = []
                    selected_index = 0
                    state = "battle_select_2"
                else:
                    battle_team_2 = chosen
                    state = "battle_ready"

        if state == "battle_ready":
            wait_for_enter("battle_start", "배틀을 시작합니다! 엔터를 누르세요.")

        if state == "battle_start":
            p1_team = battle_team_1[:3]
            p2_team = battle_team_2[:3]
            p1_current = 0
            p2_current = 0
            p1_current_pokemon_id = 0
            p2_current_pokemon_id = 0
            p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
            p2_team[p2_current_pokemon_id]["current_status"][0] = p2_team[p2_current_pokemon_id]["current_status"][0]
            state = "battle_turn"
            p1_l_screen = False
            p1_l_screen_timer=0
            p1_reflect = False
            p1_reflect_timer=0
            p2_l_screen = False
            p2_l_screen_timer=0
            p2_reflect = False
            p2_reflect_timer=0
            weather=None
            weather_timer=0
            field=None
            field_timer=0
            trick_room=False
            trick_room_timer=0
            wonder_room=False
            wonder_room_timer=0
            gravity=False
            gravity_timer=0
            draw_battle_screen(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id], p1_team[p1_current_pokemon_id]['current_status'][0], p2_team[p2_current_pokemon_id]["current_status"][0])
            p1_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (
                        2 + max(p1_team[p1_current_pokemon_id]["rank"][4], 0)) / (
                               2 - min(p1_team[p1_current_pokemon_id]["rank"][4], 0)) * (
                           0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1)
            p2_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (
                        2 + max(p2_team[p2_current_pokemon_id]["rank"][4], 0)) / (
                               2 - min(p2_team[p2_current_pokemon_id]["rank"][4], 0)) * (
                           0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1)
            if p1_speed > p2_speed:
                if p1_team[p1_current_pokemon_id]['ability'] == '가뭄':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability'] == '진홍빛고동':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"코라이돈은 햇살을 강하게 하여 고대의 고동을 폭발시켰다!!")
                    weather = 'Sun'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='잔비':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "축축한바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='모래날림':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "보송보송바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='눈퍼뜨리기':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "차가운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='일렉트릭메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에 전기가 떠돌기 시작했다!")
                    field = 'Electric'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='하드론엔진':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"미라이돈은 일렉트릭필드를 전개하여 미래 기관을 가동했다!!")
                    field = 'Electric'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='사이코메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에서 이상한 느낌이 든다!")
                    field = 'Psyco'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='그래스메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에 풀이 무성해졌다!")
                    field = 'Grass'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='미스트메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑이 안개로 자욱해졌다!")
                    field = 'Mist'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='위협' and not p2_team[p2_current_pokemon_id]['ability']=='황금몸':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    p2_team[p2_current_pokemon_id]['rank'][0]-=1

                if p2_team[p2_current_pokemon_id]['ability'] == '가뭄':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability'] == '진홍빛고동':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"코라이돈은 햇살을 강하게 하여 고대의 고동을 폭발시켰다!!")
                    weather = 'Sun'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='잔비':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "축축한바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='모래날림':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "보송보송바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='눈퍼뜨리기':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "차가운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='일렉트릭메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에 전기가 떠돌기 시작했다!")
                    field = 'Electric'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='하드론엔진':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"미라이돈은 일렉트릭필드를 전개하여 미래 기관을 가동했다!!")
                    field = 'Electric'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='사이코메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에서 이상한 느낌이 든다!")
                    field = 'Psyco'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='그래스메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에 풀이 무성해졌다!")
                    field = 'Grass'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='미스트메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑이 안개로 자욱해졌다!")
                    field = 'Mist'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='위협' and not p1_team[p1_current_pokemon_id]['ability']=='황금몸':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    p1_team[p1_current_pokemon_id]['rank'][0]-=1
            else:
                if p2_team[p2_current_pokemon_id]['ability'] == '가뭄':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability'] == '진홍빛고동':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"코라이돈은 햇살을 강하게 하여 고대의 고동을 폭발시켰다!!")
                    weather = 'Sun'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='잔비':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "축축한바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='모래날림':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "보송보송바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='눈퍼뜨리기':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "차가운바위" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='일렉트릭메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에 전기가 떠돌기 시작했다!")
                    field = 'Electric'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='하드론엔진':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"미라이돈은 일렉트릭필드를 전개하여 미래 기관을 가동했다!!")
                    field = 'Electric'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='사이코메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에서 이상한 느낌이 든다!")
                    field = 'Psyco'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='그래스메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑에 풀이 무성해졌다!")
                    field = 'Grass'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='미스트메이커':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    print(f"발밑이 안개로 자욱해졌다!")
                    field = 'Mist'
                    weather_timer = (5 if not p2_team[p2_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p2_team[p2_current_pokemon_id]['ability']=='위협' and not p1_team[p1_current_pokemon_id]['ability']=='황금몸':
                    print(f'{p2_team[p2_current_pokemon_id]["name"]} - {p2_team[p2_current_pokemon_id]["ability"]}')
                    p1_team[p1_current_pokemon_id]['rank'][0]-=1

                if p1_team[p1_current_pokemon_id]['ability'] == '가뭄':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability'] == '진홍빛고동':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"코라이돈은 햇살을 강하게 하여 고대의 고동을 폭발시켰다!!")
                    weather = 'Sun'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "뜨거운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='잔비':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "축축한바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='모래날림':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "보송보송바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='눈퍼뜨리기':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "차가운바위" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='일렉트릭메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에 전기가 떠돌기 시작했다!")
                    field = 'Electric'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='하드론엔진':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"미라이돈은 일렉트릭필드를 전개하여 미래 기관을 가동했다!!")
                    field = 'Electric'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='사이코메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에서 이상한 느낌이 든다!")
                    field = 'Psyco'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='그래스메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑에 풀이 무성해졌다!")
                    field = 'Grass'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='미스트메이커':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    print(f"발밑이 안개로 자욱해졌다!")
                    field = 'Mist'
                    weather_timer = (5 if not p1_team[p1_current_pokemon_id]['item'] == "그라운드코트" else 8)
                elif p1_team[p1_current_pokemon_id]['ability']=='위협' and not p2_team[p2_current_pokemon_id]['ability']=='황금몸':
                    print(f'{p1_team[p1_current_pokemon_id]["name"]} - {p1_team[p1_current_pokemon_id]["ability"]}')
                    p2_team[p2_current_pokemon_id]['rank'][0]-=1
        while state == "battle_turn":
            p1_team[p1_current_pokemon_id]['Flinch']=0
            p2_team[p2_current_pokemon_id]['Flinch']=0
            p1_team[p1_current_pokemon_id]['turn'] += 1
            p2_team[p2_current_pokemon_id]['turn'] += 1
            draw_battle_screen(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id], p1_team[p1_current_pokemon_id]['current_status'][0], p2_team[p2_current_pokemon_id]["current_status"][0])
            pygame.time.delay(800)
            p1_fainted_flag=0
            p2_fainted_flag=0
            p1_charge=0
            p2_charge=0
            ca=1
            while ca:
                p1_action=choose_action(1)
                if p1_action=='교체':
                    chosen_pokemon,p1_idx,ca=choose_pokemon(1,p1_team,p1_current_pokemon_id)
                else:
                    if p1_team[p1_current_pokemon_id]['next_move']:
                        p1_move_choice = p1_team[p1_current_pokemon_id]['next_move']['name']
                        move1=p1_team[p1_current_pokemon_id]['next_move']
                        p1_charge=1
                        ca=0
                    elif p1_team[p1_current_pokemon_id]["PP"][0] or p1_team[p1_current_pokemon_id]["PP"][1] or p1_team[p1_current_pokemon_id]["PP"][2] or p1_team[p1_current_pokemon_id]["PP"][3]:
                        p1_move_choice, p1_choose_move_index,ca = choose_move(1, p1_team[p1_current_pokemon_id])
                    else:
                        p1_move_choice = "발버둥"
                        ca=0
                    move1 = find_move(p1_move_choice)
            ca=1
            while ca:
                p2_action = choose_action(2)
                if p2_action == '교체':
                    chosen_pokemon, p2_idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                else:
                    if p2_team[p2_current_pokemon_id]['next_move']:
                        p2_move_choice = p2_team[p2_current_pokemon_id]['next_move']['name']
                        move2=p2_team[p2_current_pokemon_id]['next_move']
                        p2_charge=1
                        ca=0
                    elif p2_team[p2_current_pokemon_id]["PP"][0] or p2_team[p2_current_pokemon_id]["PP"][1] or p2_team[p2_current_pokemon_id]["PP"][2] or p2_team[p2_current_pokemon_id]["PP"][3]:
                        p2_move_choice,p2_choose_move_index,ca = choose_move(2, p2_team[p2_current_pokemon_id])
                    else:
                        p2_move_choice = "발버둥"
                        ca=0
                    move2 = find_move(p2_move_choice)
            if p1_action=="교체" and p2_action=='교체':
                if trick_room:
                    p2_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (2 + max(p1_team[p1_current_pokemon_id]["rank"][4],0)) / (
                                2 - min(p1_team[p1_current_pokemon_id]["rank"][4],0)) * (0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1)
                    p1_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (2 + max(p2_team[p2_current_pokemon_id]["rank"][4],0)) / (
                                2 - min(p2_team[p2_current_pokemon_id]["rank"][4],0)) * (0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1)
                else:
                    p1_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (2 + max(p1_team[p1_current_pokemon_id]["rank"][4],0)) / (
                                2 - min(p1_team[p1_current_pokemon_id]["rank"][4],0)) * (0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1)
                    p2_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (2 + max(p2_team[p2_current_pokemon_id]["rank"][4],0)) / (
                                2 - min(p2_team[p2_current_pokemon_id]["rank"][4],0)) * (0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1)
                if p1_speed > p2_speed:
                    p1_team[p1_current_pokemon_id]["rank"]=[0,0,0,0,0,0,0,0]
                    p1_current_pokemon_id = p1_idx
                    p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]

                    p2_team[p2_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                    p2_current_pokemon_id = p2_idx
                    p2_team[p2_current_pokemon_id]["current_status"][0] = p2_team[p2_current_pokemon_id]["current_status"][0]
                else:
                    p2_team[p2_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                    p2_current_pokemon_id = p2_idx
                    p2_team[p2_current_pokemon_id]["current_status"][0] = p2_team[p2_current_pokemon_id]["current_status"][0]

                    p1_team[p1_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                    p1_current_pokemon_id = p1_idx
                    p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
            elif p1_action=='교체':
                p1_team[p1_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                p1_current_pokemon_id = p1_idx
                p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]

                attacker_num,attacker,move_name,move_data=(2,p2_team[p2_current_pokemon_id],p2_move_choice,move2)
                defender=p1_team[p1_current_pokemon_id]
                defender_hp=p1_team[p1_current_pokemon_id]['current_status'][0]
                if move_data['name']=='솔라빔' and p2_charge==0:
                    if not weather=='Sun':
                        p2_team[p2_current_pokemon_id]['next_move']=move_data
                        print(f"{attacker['name']}의 솔라빔!")
                        print(f"{attacker['name']}은(는) 햇빛을 모으기 시작했다!")
                        continue
                if move_name == '쾌청':
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not attacker['item'] == "뜨거운바위" else 8)
                    continue
                if move_name == '비바라기':
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not attacker['item'] == "축축한바위" else 8)
                    continue
                if move_name == '모래바람':
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not attacker['item'] == "보송보송바위" else 8)
                    continue
                if move_name == '설경':
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not attacker['item'] == "차가운바위" else 8)
                    continue
                if move_name == '리플렉터':
                    if attacker_num == 1:
                        p1_reflect = True
                        p1_reflect_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    else:
                        p2_reflect = True
                        p2_reflect_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    continue
                if move_name == '빛의장막':
                    if attacker_num == 1:
                        p1_l_screen = True
                        p1_l_screen_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    else:
                        p2_l_screen = True
                        p2_l_screen_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    continue
                if move_name == '트릭룸':
                    trick_room = True
                    trick_room_timer = (5 if not attacker['item'] == '룸서비스' else 8)
                    continue
                if move_name == '원더룸':
                    wonder_room = True
                    wonder_room_timer = (5 if not attacker['item'] == '룸서비스' else 8)
                    continue
                if "방어" in move_data['property']:
                    print(f"{attacker['name']}의 {move_name}!")
                    print("하지만 실패했다!")
                    continue
                if move_data['category'] == '변화':
                    par_flag, flinch_flag, except_flag = 0, 0, 0
                    if random.random() < int(move_data["accuracy"]) / 100 * (
                            (3 + max(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]])))) / (
                            3 - min(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]]))))):
                        hit=1
                        if attacker["status"] == "Paralysis" and random.random() < 25:
                            print(f"{attacker['name']}의 {move_name}!")
                            print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                            continue
                        if attacker['Flinch']:
                            hit = 0
                            print(f"{attacker['name']}은(는) 풀이 죽어 기술을 쓸 수 없다!")
                            continue
                        if int(move_data['priority']) and field == 'Psyco' and not (
                                ('비행' in defender["type"] or defender['ability'] == '부유') and not gravity):
                            hit = 0
                            except_flag = 1
                            print(f"{attacker['name']}의 {move_name}!")
                            print(f"사이코필드가 {defender['name']}을(를) 지켜냈다!")
                            continue
                        print(f"{attacker['name']}의 {move_name}!")
                        p1_team[p1_current_pokemon_id]=(
                            another_effect(p2_team[p2_current_pokemon_id], p1_team[p1_current_pokemon_id], move_data, hit))
                        p2_team[p2_current_pokemon_id]['rank']=side_effect(p2_team[p2_current_pokemon_id], move_data, hit)
                        continue
                    else:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"하지만 빗나갔다!")
                        continue

                dmg, hit, type_mult, is_crit, par_flag, flinch_flag, except_flag = calculate_damage(attacker, defender,
                                                                                                    move_data,
                                                                                                    weather=weather,
                                                                                                    reflect=p1_reflect if attacker_num == 1 else p2_reflect,
                                                                                                    l_screen=p1_l_screen if attacker_num == 1 else p2_l_screen,
                                                                                                    field=field,
                                                                                                    gravity=gravity,
                                                                                                    wonder_room=wonder_room)
                p2_team[p2_current_pokemon_id]['next_move']=None
                p2_charge=0
                if dmg>defender['current_status'][0]:
                    dmg=defender['current_status'][0]
                if not hit and par_flag:
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                    continue
                if not hit and flinch_flag:
                    attacker['Flinch'] = 0
                    continue
                if not hit and except_flag == 0:
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"하지만 빗나갔다!")
                    continue
                if not hit:
                    continue

                if hit and not move_name == '발버둥':
                    attacker['PP'][p2_choose_move_index] -= 1
                p1_team[p1_current_pokemon_id]['current_status'][0] -= dmg
                print(f"{attacker['name']}의 {move_name}!") if not move_name == "발버둥" else print(
                    f"{attacker['name']}는 발버둥을 썼다!")
                if type_mult == 0:
                    print("효과가 없는 것 같다...")
                elif type_mult > 1:
                    print("효과가 굉장했다!")
                    if is_crit:
                        print("급소에 맞았다!")
                elif 0 < type_mult < 1:
                    print("효과가 별로인 듯하다...")
                    if is_crit:
                        print("급소에 맞았다!")
                else:
                    if is_crit:
                        print("급소에 맞았다!")
                another_effect(p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id], defender, move_data, hit)
                (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['rank']=side_effect(p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id], move_data, hit)
                if '접촉' in move_data['property'] and p1_team[p1_current_pokemon_id][
                    'status'] == None and random.random() <= 0.3 and attacker['ability'] == '독수' and not defender['ability']=='황금몸':
                    print(f'{attacker["name"]} - 독수')
                    print(f'{defender["name"]}의 몸에 독이 퍼졌다!')
                    p1_team[p1_current_pokemon_id]['status'] = "Poison"
                if p1_team[p1_current_pokemon_id]['current_status'][0] <= 0:
                    p1_team[p1_current_pokemon_id]['current_status'][0] = 0
                    print(f"{defender['name']}은(는) 기절했다!")
                if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                    ca = 1
                    while ca:
                        a, idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                    p1_current_pokemon_id = idx
                    p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                    wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                    p1_fainted_flag = 1
                    p1_current+=1
                    p2_team[p2_current_pokemon_id]['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                    if attacker['item']=='생명의구슬':
                        print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                        p2_team[p2_current_pokemon_id]['current_status'][0]-=p2_team[p2_current_pokemon_id]['current_status'][0]//10
                    break
                elif p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                    print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                    print("플레이어 2 승!")
                    exit()
                (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['current_status'][0] -= rebound_calculate(attacker, dmg, move_data, hit)
                if attacker['item']=='생명의구슬':
                    print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                    p2_team[p2_current_pokemon_id]['current_status'][0]-=p2_team[p2_current_pokemon_id]['current_status'][0]//10
                draw_battle_screen(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id], p1_team[p1_current_pokemon_id]['current_status'][0], p2_team[p2_current_pokemon_id]["current_status"][0])
                pygame.display.flip()
                time.sleep(1.5)

                if p1_team[p1_current_pokemon_id]['current_status'][0] if attacker_num == 1 else p2_team[p2_current_pokemon_id]['current_status'][0] <= 0:
                    if attacker_num ==1:
                        p1_team[p1_current_pokemon_id]['current_status'][0]=0
                    else:
                        p2_team[p2_current_pokemon_id]['current_status'][0] = 0
                    print(f"{defender['name']}은(는) 기절했다!")
                if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                    ca = 1
                    while ca:
                        a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                    p2_current_pokemon_id = idx
                    wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                    p2_current+=1
                    p2_fainted_flag = 1
                    break
                elif p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                    print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                    print("플레이어 1 승!")
                    exit()
                if int(move_data["return"]) and p2_current<2:
                    ca=1
                    while ca:
                        chosen_pokemon, p2_idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                    p2_team[p2_current_pokemon_id]["turn"]=0
                    p2_team[p2_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                    p2_current_pokemon_id = p2_idx
                    p2_team[p2_current_pokemon_id]["current_status"][0] = \
                    p2_team[p2_current_pokemon_id]["current_status"][0]
                if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 or p2_team[p2_current_pokemon_id]["current_status"][0] == 0:
                    break
            elif p2_action=='교체':
                p2_team[p2_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                p2_current_pokemon_id = p2_idx
                p2_team[p2_current_pokemon_id]["current_status"][0] = p2_team[p2_current_pokemon_id]["current_status"][0]

                attacker_num, attacker, move_name, move_data = (1, p1_team[p1_current_pokemon_id], p1_move_choice, move1)
                defender = p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id]
                defender_hp = p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]
                if move_data['name']=='솔라빔' and p1_charge==0:
                    if not weather=='Sun':
                        p1_team[p1_current_pokemon_id]['next_move']=move_data
                        print(f"{attacker['name']}의 솔라빔!")
                        print(f"{attacker['name']}은(는) 햇빛을 모으기 시작했다!")
                        continue
                if move_name == '쾌청':
                    print(f"{attacker['name']}의 {move_name}!")
                    print("햇살이 강해졌다!")
                    weather = 'Sun'
                    weather_timer = (5 if not attacker['item'] == "뜨거운바위" else 8)
                    continue
                if move_name == '비바라기':
                    print(f"{attacker['name']}의 {move_name}!")
                    print("비가 내리기 시작했다!")
                    weather = 'Rain'
                    weather_timer = (5 if not attacker['item'] == "축축한바위" else 8)
                    continue
                if move_name == '모래바람':
                    print(f"{attacker['name']}의 {move_name}!")
                    print("모래바람이 불기 시작했다!")
                    weather = 'SandStorm'
                    weather_timer = (5 if not attacker['item'] == "보송보송바위" else 8)
                    continue
                if move_name == '설경':
                    print(f"{attacker['name']}의 {move_name}!")
                    print("눈이 내리기 시작했다!")
                    weather = 'Snow'
                    weather_timer = (5 if not attacker['item'] == "차가운바위" else 8)
                    continue
                if move_name == '리플렉터':
                    if attacker_num == 1:
                        p1_reflect = True
                        p1_reflect_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    else:
                        p2_reflect = True
                        p2_reflect_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                if move_name == '빛의장막':
                    if attacker_num == 1:
                        p1_l_screen = True
                        p1_l_screen_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                    else:
                        p2_l_screen = True
                        p2_l_screen_timer = (5 if not attacker['item'] == "빛의점토" else 8)
                if move_name == '트릭룸':
                    trick_room = True
                    trick_room_timer = (5 if not attacker['item'] == '룸서비스' else 8)
                if move_name == '원더룸':
                    wonder_room = True
                    wonder_room_timer = (5 if not attacker['item'] == '룸서비스' else 8)
                if "방어" in move_data['property']:
                    print(f"{attacker['name']}의 {move_name}!")
                    print("하지만 실패했다!")
                    continue
                if move_data['category'] == '변화':
                    par_flag, flinch_flag, except_flag = 0, 0, 0
                    if random.random() < int(move_data["accuracy"]) / 100 * (
                            (3 + max(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]])))) / (
                            3 - min(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]]))))):
                        hit=1
                        if attacker["status"] == "Paralysis" and random.random() < 25:
                            print(f"{attacker['name']}의 {move_name}!")
                            print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                            continue
                        if attacker['Flinch']:
                            hit = 0
                            print(f"{attacker['name']}은(는) 풀이 죽어 기술을 쓸 수 없다!")
                            continue
                        if int(move_data['priority']) and field == 'Psyco' and not (
                                ('비행' in defender["type"] or defender['ability'] == '부유') and not gravity):
                            hit = 0
                            except_flag = 1
                            print(f"{attacker['name']}의 {move_name}!")
                            print(f"사이코필드가 {defender['name']}을(를) 지켜냈다!")
                            continue
                        print(f"{attacker['name']}의 {move_name}!")
                        p2_team[p2_current_pokemon_id]=another_effect(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id], move_data, hit)
                        p1_team[p1_current_pokemon_id]['rank']=side_effect(p1_team[p1_current_pokemon_id], move_data, hit)
                        continue
                    else:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"하지만 빗나갔다!")
                        continue
                dmg, hit, type_mult, is_crit, par_flag, flinch_flag, except_flag = calculate_damage(attacker, defender,
                                                                                                    move_data,
                                                                                                    weather=weather,
                                                                                                    reflect=p1_reflect if attacker_num == 1 else p2_reflect,
                                                                                                    l_screen=p1_l_screen if attacker_num == 1 else p2_l_screen,
                                                                                                    field=field,
                                                                                                    gravity=gravity,
                                                                                                    wonder_room=wonder_room)
                p1_team[p1_current_pokemon_id]['next_move'] = None
                p1_charge = 0
                if dmg>defender['current_status'][0]:
                    dmg=defender['current_status'][0]
                if not hit and par_flag:
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                    continue
                if not hit and flinch_flag:
                    if attacker_num==1:
                        p1_team[p1_current_pokemon_id]['Flinch']=0
                    else:
                        p2_team[p2_current_pokemon_id]['Flinch']=0
                    continue
                if not hit and except_flag == 0:
                    print(f"{attacker['name']}의 {move_name}!")
                    print(f"하지만 빗나갔다!")
                    continue
                if not hit:
                    continue

                if hit and not move_name == '발버둥':
                    (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])['current_status'][0] -= dmg
                print(f"{attacker['name']}의 {move_name}!") if not move_name == "발버둥" else print(
                    f"{attacker['name']}는 발버둥을 썼다!")
                if type_mult == 0:
                    print("효과가 없는 것 같다...")
                elif type_mult > 1:
                    print("효과가 굉장했다!")
                    if is_crit:
                        print("급소에 맞았다!")
                elif 0 < type_mult < 1:
                    print("효과가 별로인 듯하다...")
                    if is_crit:
                        print("급소에 맞았다!")
                else:
                    if is_crit:
                        print("급소에 맞았다!")
                p2_team[p2_current_pokemon_id]=another_effect(attacker, defender, move_data, hit)
                (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['rank']=side_effect(p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id], move_data, hit)
                if (p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]) <= 0:
                    (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])['current_status'][0] = 0
                    print(f"{defender['name']}은(는) 기절했다!")
                if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                    ca = 1
                    while ca:
                        a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                    p2_current_pokemon_id = idx
                    wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                    p2_current += 1
                    p2_fainted_flag = 1
                    if attacker['item']=='생명의구슬':
                        print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0]-=p1_team[p1_current_pokemon_id]['current_status'][0]//10
                    (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                    break
                elif p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                    print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                    print("플레이어 1 승!")
                    exit()
                (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                if attacker['item']=='생명의구슬':
                    print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                    (p1_team[p1_current_pokemon_id] if attacker_num==1 else p2_team[p2_current_pokemon_id])['current_status'][0]-=(p1_team[p1_current_pokemon_id] if attacker_num==1 else p2_team[p2_current_pokemon_id])['current_status'][0]//10

                draw_battle_screen(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id], p1_team[p1_current_pokemon_id]['current_status'][0], p2_team[p2_current_pokemon_id]["current_status"][0])
                pygame.display.flip()
                time.sleep(1.5)

                if (p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else
                p1_team[p1_current_pokemon_id]['current_status'][0]) <= 0:
                    (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])[
                        'current_status'][0] = 0
                    print(f"{defender['name']}은(는) 기절했다!")
                if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                    ca = 1
                    while ca:
                        a, idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                    p1_current_pokemon_id = idx
                    p1_team[p1_current_pokemon_id]['current_status'][0] = \
                    p1_team[p1_current_pokemon_id]["current_status"][0]
                    wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                    p1_fainted_flag = 1
                    break
                elif p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                    print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                    print("플레이어 2 승!")
                    exit()
                if int(move_data["return"]) and p1_current<2:
                    ca = 1
                    while ca:
                        chosen_pokemon, p1_idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                    p1_team[p1_current_pokemon_id]["turn"] = 0
                    p1_team[p1_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                    p1_current_pokemon_id = p1_idx
                    p1_team[p1_current_pokemon_id]['current_status'][0] = \
                    p1_team[p1_current_pokemon_id]["current_status"][0]
                if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 or p2_team[p2_current_pokemon_id]["current_status"][0] == 0:
                    break
            else:
                if move1["priority"] > move2["priority"]:
                    first,second = ((1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,1),
                                    (2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,2))
                elif move1["priority"] < move2["priority"]:
                    first,second = ((2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,1),
                                    (1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,2))
                else:
                    if trick_room:
                        p2_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (
                                    2 + max(p1_team[p1_current_pokemon_id]["rank"][4], 0)) / (
                                           2 - min(p1_team[p1_current_pokemon_id]["rank"][4], 0)) * (
                                       0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                                       1.5 if p2_team[p2_current_pokemon_id]['ability'] == '고대활성' and
                                              p2_team[p2_current_pokemon_id]['max_status'][1:6].index(
                                                  max(p2_team[p2_current_pokemon_id]['max_status'][1:6])) == 5 and
                                              weather == 'Sun' else 1)
                        p1_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (
                                    2 + max(p2_team[p2_current_pokemon_id]["rank"][4], 0)) / (
                                           2 - min(p2_team[p2_current_pokemon_id]["rank"][4], 0)) * (
                                       0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                                       1.5 if p1_team[p1_current_pokemon_id]['ability'] == '고대활성' and
                                              p1_team[p1_current_pokemon_id]['max_status'][1:6].index(
                                                  max(p1_team[p1_current_pokemon_id]['max_status'][1:6])) == 5 and
                                              weather == 'Sun' else 1)
                    else:
                        p1_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (
                                    2 + max(p1_team[p1_current_pokemon_id]["rank"][4], 0)) / (
                                           2 - min(p1_team[p1_current_pokemon_id]["rank"][4], 0)) * (
                                       0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                                       1.5 if p1_team[p1_current_pokemon_id]['ability'] == '고대활성' and
                                              p1_team[p1_current_pokemon_id]['max_status'][1:6].index(
                                                  max(p1_team[p1_current_pokemon_id]['max_status'][1:6])) == 5 and
                                              weather == 'Sun' else 1)
                        p2_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (
                                    2 + max(p2_team[p2_current_pokemon_id]["rank"][4], 0)) / (
                                           2 - min(p2_team[p2_current_pokemon_id]["rank"][4], 0)) * (
                                       0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                                       1.5 if p2_team[p2_current_pokemon_id]['ability'] == '고대활성' and
                                              p2_team[p2_current_pokemon_id]['max_status'][1:6].index(
                                                  max(p2_team[p2_current_pokemon_id]['max_status'][1:6])) == 5 and
                                              weather == 'Sun' else 1)
                    if p1_speed > p2_speed:
                        first, second = ((1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,1),
                                         (2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,2))
                    elif p1_speed < p2_speed:
                        first, second = ((2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,1),
                         (1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,2))
                    else:
                        if random.randint(1,2)==1:
                            first, second = ((1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,1),
                                             (2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,2))
                        else:
                            first, second = ((2, p2_team[p2_current_pokemon_id], p2_move_choice, move2,1),
                                             (1, p1_team[p1_current_pokemon_id], p1_move_choice, move1,2))

                for turn in [first, second]:
                    attacker_num, attacker, move_name, move_data,fs = turn
                    defender = p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id]
                    defender_hp = p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]
                    if move_data['name'] == '솔라빔' and (p1_charge if attacker_num==1 else p2_charge) == 0:
                        if not weather == 'Sun':
                            (p1_team if attacker_num==1 else p2_team)[p1_current_pokemon_id if attacker_num==1 else p2_current_pokemon_id]['next_move'] = move_data
                            print(f"{attacker['name']}의 솔라빔!")
                            print(f"{attacker['name']}은(는) 햇빛을 모으기 시작했다!")
                            continue
                    if move_name=='쾌청':
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"햇살이 강해졌다!")
                        weather='Sun'
                        weather_timer=(5 if not attacker['item']=="뜨거운바위" else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if move_name=='비바라기':
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"비가 내리기 시작했다!")
                        weather='Rain'
                        weather_timer=(5 if not attacker['item']=="축축한바위" else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if move_name=='모래바람':
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"모래바람이 불기 시작했다!")
                        weather='SandStorm'
                        weather_timer=(5 if not attacker['item']=="보송보송바위" else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if move_name=='설경':
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"눈이 내리기 시작했다!")
                        weather='Snow'
                        weather_timer=(5 if not attacker['item']=="차가운바위" else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if move_name=='리플렉터':
                        if attacker_num == 1:
                            p1_reflect=True
                            p1_reflect_timer=(5 if not attacker['item']=="빛의점토" else 8)
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])[
                                'PP'][
                                p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        else:
                            p2_reflect=True
                            p2_reflect_timer=(5 if not attacker['item']=="빛의점토" else 8)
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])[
                                'PP'][
                                p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                    if move_name=='빛의장막':
                        if attacker_num == 1:
                            p1_l_screen=True
                            p1_l_screen_timer=(5 if not attacker['item']=="빛의점토" else 8)
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])[
                                'PP'][
                                p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        else:
                            p2_l_screen=True
                            p2_l_screen_timer=(5 if not attacker['item']=="빛의점토" else 8)
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])[
                                'PP'][
                                p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                    if move_name=='트릭룸':
                        trick_room=True
                        trick_room_timer=(5 if not attacker['item']=='룸서비스' else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                    if move_name=='원더룸':
                        wonder_room = True
                        wonder_room_timer = (5 if not attacker['item'] == '룸서비스' else 8)
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                    if "방어" in move_data['property'] and fs==2:
                        print(f"{attacker['name']}의 {move_name}!")
                        print("하지만 실패했다!")
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    elif "방어" in move_data['property']:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"{attacker['name']}은(는) 방어 태세에 돌입했다!")
                        ((p1_team if attacker_num == 1 else p2_team)[p1_current_pokemon_id if attacker_num==1 else p2_current_pokemon_id])['protect'] = True
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if move_data['category'] == '변화':
                        par_flag, flinch_flag, except_flag = 0, 0, 0
                        if random.random() < int(move_data["accuracy"]) / 100 * (
                                (3 + max(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]])))) / (
                                3 - min(0, int(numpy.median([-6, 6, attacker["rank"][5] - defender["rank"][6]]))))) or int(move_data['accuracy'])==-1:
                            hit = 1
                            if attacker["status"] == "Paralysis" and random.random() < 25:
                                print(f"{attacker['name']}의 {move_name}!")
                                print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                                continue
                            if attacker['Flinch']:
                                hit = 0
                                print(f"{attacker['name']}은(는) 풀이 죽어 기술을 쓸 수 없다!")
                                continue
                            if int(move_data['priority']) and field == 'Psyco' and not (
                                    ('비행' in defender["type"] or defender['ability'] == '부유') and not gravity):
                                hit = 0
                                except_flag = 1
                                print(f"{attacker['name']}의 {move_name}!")
                                print(f"사이코필드가 {defender['name']}을(를) 지켜냈다!")
                                continue
                            print(f"{attacker['name']}의 {move_name}!")
                            if defender['protect'] and another_effect((p1_team[p1_current_pokemon_id] if attacker_num ==1 else p2_team[p2_current_pokemon_id]),
                                                                                (p2_team[p2_current_pokemon_id] if attacker_num ==1 else p1_team[p1_current_pokemon_id]), move_data,
                                                                                hit) == (p2_team if attacker_num==1 else p1_team)[p2_current_pokemon_id if attacker_num==1 else p1_current_pokemon_id]:
                                print(f"{attacker['name']}의 {move_name}!")
                                print(f"{defender['name']}은(는) 공격으로부터 몸을 지켜냈다!")
                                (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[
                                    p2_current_pokemon_id])['PP'][
                                    p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                                continue
                            else:
                                (p2_team if attacker_num==1 else p1_team)[p2_current_pokemon_id if attacker_num==1 else p1_current_pokemon_id] = another_effect((p1_team[p1_current_pokemon_id] if attacker_num ==1 else p2_team[p2_current_pokemon_id]),
                                                                                (p2_team[p2_current_pokemon_id] if attacker_num ==1 else p1_team[p1_current_pokemon_id]), move_data,
                                                                                hit)
                            (p1_team[p1_current_pokemon_id] if attacker_num ==1 else p2_team[p2_current_pokemon_id])['rank'] = side_effect((p1_team[p1_current_pokemon_id] if attacker_num ==1 else p2_team[p2_current_pokemon_id]),
                                                                                 move_data, hit)
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])[
                                'PP'][
                                p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                            continue
                        else:
                            print(f"{attacker['name']}의 {move_name}!")
                            print(f"하지만 빗나갔다!")
                            continue
                    if defender['protect']:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"{defender['name']}은(는) 공격으로부터 몸을 지켜냈다!")
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    dmg, hit, type_mult, is_crit, par_flag, flinch_flag, except_flag = calculate_damage(attacker, defender, move_data,
                                                                                           weather=weather,
                                                                                           reflect=p1_reflect if attacker_num == 1 else p2_reflect,
                                                                                           l_screen=p1_l_screen if attacker_num == 1 else p2_l_screen,
                                                                                           field=field, gravity=gravity, wonder_room=wonder_room)
                    (p1_team if attacker_num==1 else p2_team)[p1_current_pokemon_id if attacker_num==1 else p2_current_pokemon_id]['next_move'] = None
                    if attacker_num == 1:
                        p1_charge=0
                    else:
                        p2_charge=0
                    if dmg>defender['current_status'][0]:
                        dmg=defender['current_status'][0]
                    if not hit and par_flag:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"{attacker['name']}은(는) 몸이 저려서 움직일 수 없다!")
                        continue
                    if not hit and flinch_flag:
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['Flinch'] = 0
                        continue
                    if not hit and except_flag==0:
                        print(f"{attacker['name']}의 {move_name}!")
                        print(f"하지만 빗나갔다!")
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][
                            p1_choose_move_index if attacker_num == 1 else p2_choose_move_index] -= 1
                        continue
                    if not hit:
                        continue
                    if hit and not move_name=='발버둥':
                        (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['PP'][p1_choose_move_index if attacker_num==1 else p2_choose_move_index]-=1
                    if attacker_num==1:
                        p2_team[p2_current_pokemon_id]["current_status"][0]-=dmg
                    else:
                        p1_team[p1_current_pokemon_id]['current_status'][0]-=dmg
                    print(f"{attacker['name']}의 {move_name}!") if not move_name=="발버둥"else print(f"{attacker['name']}는 발버둥을 썼다!")
                    if type_mult == 0:
                        print("효과가 없는 것 같다...")
                    elif type_mult > 1:
                        print("효과가 굉장했다!")
                        if is_crit:
                            print("급소에 맞았다!")
                    elif 0 < type_mult < 1:
                        print("효과가 별로인 듯하다...")
                        if is_crit:
                            print("급소에 맞았다!")
                    else:
                        if is_crit:
                            print("급소에 맞았다!")
                    another_effect(attacker, defender, move_data, hit)
                    side_effect(attacker,move_data, hit)
                    draw_battle_screen(p1_team[p1_current_pokemon_id], p2_team[p2_current_pokemon_id],
                                       p1_team[p1_current_pokemon_id]['current_status'][0],
                                       p2_team[p2_current_pokemon_id]["current_status"][0])
                    pygame.display.flip()
                    time.sleep(1.5)
                    if attacker_num == 1:
                        if (p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]) <= 0:
                            (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])['current_status'][0] = 0
                            print(f"{defender['name']}은(는) 기절했다!")
                        if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                            ca = 1
                            while ca:
                                a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                            p2_current_pokemon_id = idx
                            p1_team[p1_current_pokemon_id]['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                            if attacker['item']=='생명의구슬':
                                print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                                p1_team[p1_current_pokemon_id]['current_status'][0]-=p1_team[p1_current_pokemon_id]['current_status'][0]//10
                            wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                            p2_current += 1
                            p2_fainted_flag = 1
                            break
                        elif p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                            print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                            print("플레이어 1 승!")
                            exit()
                    else:
                        if (p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]) <= 0:
                            (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])['current_status'][0] = 0
                            print(f"{defender['name']}은(는) 기절했다!")
                        if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                            ca = 1
                            while ca:
                                a, idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                            p1_current_pokemon_id = idx
                            p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                            p2_team[p2_current_pokemon_id]['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                            if attacker['item']=='생명의구슬':
                                print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                                p2_team[p2_current_pokemon_id]['current_status'][0]-=p2_team[p2_current_pokemon_id]['current_status'][0]//10
                            wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                            p1_fainted_flag = 1
                            break
                        elif p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                            print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                            print("플레이어 2 승!")
                            exit()
                    (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])['current_status'][0]-=rebound_calculate(attacker, dmg, move_data, hit)
                    if attacker['item']=='생명의구슬':
                        print(f'{attacker["name"]}은(는) 생명이 조금 깎였다!')
                        (p1_team[p1_current_pokemon_id] if attacker_num==1 else p2_team[p2_current_pokemon_id])['current_status'][0]-=(p1_team[p1_current_pokemon_id] if attacker_num==1 else p2_team[p2_current_pokemon_id])['current_status'][0]//10

                    if attacker_num == 2:
                        if (p1_team[p1_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p2_team[p2_current_pokemon_id]["current_status"][0]) <= 0:
                            (p1_team[p1_current_pokemon_id] if attacker_num == 1 else p2_team[p2_current_pokemon_id])["current_status"][0] = 0
                            print(f"{defender['name']}은(는) 기절했다!")
                        if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                            ca = 1
                            while ca:
                                a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                            p2_current_pokemon_id = idx
                            wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                            p2_current += 1
                            p2_fainted_flag = 1
                            break
                        elif p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                            print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                            print("플레이어 1 승!")
                            exit()
                    else:
                        if (p2_team[p2_current_pokemon_id]["current_status"][0] if attacker_num == 1 else p1_team[p1_current_pokemon_id]['current_status'][0]) <= 0:
                            (p2_team[p2_current_pokemon_id] if attacker_num == 1 else p1_team[p1_current_pokemon_id])['current_status'][0] = 0
                            print(f"{defender['name']}은(는) 기절했다!")
                        if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                            ca=1
                            while ca:
                                a,idx,ca=choose_pokemon(1,p1_team,p1_current_pokemon_id)
                            p1_current_pokemon_id=idx
                            p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                            wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                            p1_fainted_flag = 1
                            break
                        elif p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                            print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                            print("플레이어 2 승!")
                            exit()
                    if attacker_num == 1:
                        if int(move_data["return"]) and p1_current<2:
                            ca = 1
                            while ca:
                                chosen_pokemon,p1_idx,ca=choose_pokemon(1,p1_team,p1_current_pokemon_id)
                            p1_team[p1_current_pokemon_id]["turn"] = 0
                            p1_team[p1_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                            p1_current_pokemon_id = p1_idx
                            p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                    else:
                        if int(move_data["return"]) and p2_current<2:
                            ca = 1
                            while ca:
                                chosen_pokemon,p2_idx,ca=choose_pokemon(2,p2_team,p2_current_pokemon_id)
                            p2_team[p2_current_pokemon_id]["turn"] = 0
                            p2_team[p2_current_pokemon_id]["rank"] = [0, 0, 0, 0, 0, 0, 0, 0]
                            p2_current_pokemon_id = p2_idx
                    if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 or p2_team[p2_current_pokemon_id]["current_status"][0] == 0:
                        break
            if trick_room:
                p2_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (2 + max(p1_team[p1_current_pokemon_id]["rank"][4],0)) / (
                        2 - min(p1_team[p1_current_pokemon_id]["rank"][4],0)) * (0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                    1.5 if p2_team[p2_current_pokemon_id]['ability']=='고대활성' and
                           p2_team[p2_current_pokemon_id]['max_status'][1:6].index(max(p2_team[p2_current_pokemon_id]['max_status'][1:6]))==5 and
                           weather=='Sun' else 1)
                p1_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (2 + max(p2_team[p2_current_pokemon_id]["rank"][4],0)) / (
                        2 - min(p2_team[p2_current_pokemon_id]["rank"][4],0)) * (0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                    1.5 if p1_team[p1_current_pokemon_id]['ability']=='고대활성' and
                           p1_team[p1_current_pokemon_id]['max_status'][1:6].index(max(p1_team[p1_current_pokemon_id]['max_status'][1:6]))==5 and
                           weather=='Sun' else 1)
            else:
                p1_speed = p1_team[p1_current_pokemon_id]["current_status"][5] * (2 + max(p1_team[p1_current_pokemon_id]["rank"][4],0)) / (
                        2 - min(p1_team[p1_current_pokemon_id]["rank"][4],0)) * (0.5 if p1_team[p1_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                    1.5 if p1_team[p1_current_pokemon_id]['ability']=='고대활성' and
                           p1_team[p1_current_pokemon_id]['max_status'][1:6].index(max(p1_team[p1_current_pokemon_id]['max_status'][1:6]))==5 and
                           weather=='Sun' else 1)
                p2_speed = p2_team[p2_current_pokemon_id]["current_status"][5] * (2 + max(p2_team[p2_current_pokemon_id]["rank"][4],0)) / (
                        2 - min(p2_team[p2_current_pokemon_id]["rank"][4],0)) * (0.5 if p2_team[p2_current_pokemon_id]["status"] == "Paralysis" else 1) * (
                    1.5 if p2_team[p2_current_pokemon_id]['ability']=='고대활성' and
                           p2_team[p2_current_pokemon_id]['max_status'][1:6].index(max(p2_team[p2_current_pokemon_id]['max_status'][1:6]))==5 and
                           weather=='Sun' else 1)
            if p1_speed>p2_speed:
                if not p1_fainted_flag:
                    if field=="Grass" and not(('비행' in p1_team[p1_current_pokemon_id]["type"] or p1_team[p1_current_pokemon_id]['ability']=='부유') and not gravity):
                        print("그래스필드로 인해 체력이 회복되었다!")
                        p1_team[p1_current_pokemon_id]['current_status'][0]=p1_team[p1_current_pokemon_id]["max_status"][0]//16
                    if weather=='SandStorm' and not ('땅' in p1_team[p1_current_pokemon_id]["type"] or
                                                     '강철' in p1_team[p1_current_pokemon_id]["type"] or
                                                     '바위' in p1_team[p1_current_pokemon_id]["type"]) and not (
                            '매직가드'==p1_team[p1_current_pokemon_id]['ability'] or
                            '방진'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래숨기'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래헤치기'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래의힘'==p1_team[p1_current_pokemon_id]['ability']) and not '방진고글' == p1_team[p1_current_pokemon_id]['item']:
                        print(f"{p1_team[p1_current_pokemon_id]['name']}은(는) 모래바람으로 인해 데미지를 입었다!")
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 16
                    if p1_team[p1_current_pokemon_id]["status"] == "Burn":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 화상 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 16
                    elif p1_team[p1_current_pokemon_id]["status"] == "Poison":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 독에 의한 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 8
                    elif p1_team[p1_current_pokemon_id]["status"] == "SPoison":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 독에 의한 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= (p1_team[p1_current_pokemon_id]["max_status"][0] // 16) * p1_team[p1_current_pokemon_id]["SPoison_cnt"]
                        p1_team[p1_current_pokemon_id]["SPoison_cnt"] += 1
                    if p1_team[p1_current_pokemon_id]['current_status'][0] <= 0:
                        p1_team[p1_current_pokemon_id]['current_status'][0] = 0
                        print(f"{p1_team[p1_current_pokemon_id]['name']}은(는) 기절했다!")
                    if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                        ca = 1
                        while ca:
                            a, idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                        p1_current_pokemon_id = idx
                        p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                        wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                        p1_fainted_flag = 1
                        p1_current+=1
                    if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                        print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                        print("플레이어 2 승!")
                        exit()
                    if p1_team[p1_current_pokemon_id]['ability']=='가속' and p1_team[p1_current_pokemon_id]['turn']>=1:
                        p1_team[p1_current_pokemon_id]['rank'][4]=min(6,p1_team[p1_current_pokemon_id]['rank'][4]+1)
                if not p2_fainted_flag:
                    if field=="Grass" and not(('비행' in p2_team[p2_current_pokemon_id]["type"] or p2_team[p2_current_pokemon_id]['ability']=='부유') and not gravity):
                        print("그래스필드로 인해 체력이 회복되었다!")
                        p2_team[p2_current_pokemon_id]["current_status"][0]+=p2_team[p2_current_pokemon_id]["max_status"][0]//16
                    if weather=='SandStorm' and not ('땅' in p2_team[p2_current_pokemon_id]["type"] or
                                                     '강철' in p2_team[p2_current_pokemon_id]["type"] or
                                                     '바위' in p2_team[p2_current_pokemon_id]["type"]) and not (
                            '매직가드'==p2_team[p2_current_pokemon_id]['ability'] or
                            '방진'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래숨기'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래헤치기'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래의힘'==p2_team[p2_current_pokemon_id]['ability']) and not '방진고글' == p2_team[p2_current_pokemon_id]['item']:
                        print(f"{p2_team[p2_current_pokemon_id]['name']}은(는) 모래바람으로 인해 데미지를 입었다!")
                        p2_team[p2_current_pokemon_id]['current_status'][0] -= p2_team[p2_current_pokemon_id]["max_status"][0] // 16
                    if p2_team[p2_current_pokemon_id]["status"] == "Burn":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 화상의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= p2_team[p2_current_pokemon_id]["current_status"][0] // 16
                    elif p2_team[p2_current_pokemon_id]["status"] == "Poison":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 독의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= p2_team[p2_current_pokemon_id]["current_status"][0] // 8
                    elif p2_team[p2_current_pokemon_id]["status"] == "SPoison":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 맹독의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= (p2_team[p2_current_pokemon_id]["current_status"][0] // 16) * p2_team[p2_current_pokemon_id]["SPoison_cnt"]
                        p2_team[p2_current_pokemon_id]["SPoison_cnt"] += 1
                    if p2_team[p2_current_pokemon_id]['current_status'][0] <= 0:
                        p2_team[p2_current_pokemon_id]['current_status'][0] = 0
                        print(f"{p2_team[p2_current_pokemon_id]['name']}은(는) 기절했다!")
                    if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                        ca = 1
                        while ca:
                            a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                        p2_current_pokemon_id = idx
                        wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                        p2_current += 1
                        p2_fainted_flag = 1
                    if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                        print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                        print("플레이어 1 승!")
                        exit()
                    if p2_team[p2_current_pokemon_id]['ability'] == '가속' and p2_team[p2_current_pokemon_id][
                        'turn'] >= 1:
                        p2_team[p2_current_pokemon_id]['rank'][4] = min(6, p2_team[p2_current_pokemon_id]['rank'][
                            4] + 1)
            else:
                if not p2_fainted_flag:
                    if field=="Grass" and not(('비행' in p2_team[p2_current_pokemon_id]["type"] or p2_team[p2_current_pokemon_id]['ability']=='부유') and not gravity):
                        print("그래스필드로 인해 체력이 회복되었다!")
                        p2_team[p2_current_pokemon_id]["current_status"][0]+=p2_team[p2_current_pokemon_id]["max_status"][0]//16
                    if weather=='SandStorm' and not ('땅' in p2_team[p2_current_pokemon_id]["type"] or
                                                     '강철' in p2_team[p2_current_pokemon_id]["type"] or
                                                     '바위' in p2_team[p2_current_pokemon_id]["type"]) and not (
                            '매직가드'==p2_team[p2_current_pokemon_id]['ability'] or
                            '방진'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래숨기'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래헤치기'==p2_team[p2_current_pokemon_id]['ability'] or
                            '모래의힘'==p2_team[p2_current_pokemon_id]['ability']) and not '방진고글' == p2_team[p2_current_pokemon_id]['item']:
                        print(f"{p2_team[p2_current_pokemon_id]['name']}은(는) 모래바람으로 인해 데미지를 입었다!")
                        p2_team[p2_current_pokemon_id]['current_status'][0] -= p2_team[p2_current_pokemon_id]["max_status"][0] // 16
                    if p2_team[p2_current_pokemon_id]["status"] == "Burn":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 화상의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= p2_team[p2_current_pokemon_id]["current_status"][0] // 16
                    elif p2_team[p2_current_pokemon_id]["status"] == "Poison":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 독의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= p2_team[p2_current_pokemon_id]["current_status"][0] // 8
                    elif p2_team[p2_current_pokemon_id]["status"] == "SPoison":
                        print(f'{p2_team[p2_current_pokemon_id]["name"]}은(는) 맹독의 피해를 입고 있다!')
                        p2_team[p2_current_pokemon_id]["current_status"][0] -= (p2_team[p2_current_pokemon_id]["current_status"][0] // 16) * p2_team[p2_current_pokemon_id]["SPoison_cnt"]
                        p2_team[p2_current_pokemon_id]["SPoison_cnt"] += 1
                    if p2_team[p2_current_pokemon_id]['current_status'][0] <= 0:
                        p2_team[p2_current_pokemon_id]['current_status'][0] = 0
                        print(f"{p2_team[p2_current_pokemon_id]['name']}은(는) 기절했다!")
                    if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current < 2:
                        ca = 1
                        while ca:
                            a, idx, ca = choose_pokemon(2, p2_team, p2_current_pokemon_id)
                        p2_current_pokemon_id = idx
                        wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p2_team[p2_current_pokemon_id]['name']}")
                        p2_current += 1
                        p2_fainted_flag = 1
                    if p2_team[p2_current_pokemon_id]["current_status"][0] == 0 and p2_current >= 2:
                        print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                        print("플레이어 1 승!")
                        exit()
                    if p2_team[p2_current_pokemon_id]['ability'] == '가속' and p2_team[p2_current_pokemon_id][
                        'turn'] >= 1:
                        p2_team[p2_current_pokemon_id]['rank'][4] = min(6, p2_team[p2_current_pokemon_id]['rank'][
                            4] + 1)
                if not p1_fainted_flag:
                    if field=="Grass" and not(('비행' in p1_team[p1_current_pokemon_id]["type"] or p1_team[p1_current_pokemon_id]['ability']=='부유') and not gravity):
                        print("그래스필드로 인해 체력이 회복되었다!")
                        p1_team[p1_current_pokemon_id]['current_status'][0]=p1_team[p1_current_pokemon_id]["max_status"][0]//16
                    if weather=='SandStorm' and not ('땅' in p1_team[p1_current_pokemon_id]["type"] or
                                                     '강철' in p1_team[p1_current_pokemon_id]["type"] or
                                                     '바위' in p1_team[p1_current_pokemon_id]["type"]) and not (
                            '매직가드'==p1_team[p1_current_pokemon_id]['ability'] or
                            '방진'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래숨기'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래헤치기'==p1_team[p1_current_pokemon_id]['ability'] or
                            '모래의힘'==p1_team[p1_current_pokemon_id]['ability']) and not '방진고글' == p1_team[p1_current_pokemon_id]['item']:
                        print(f"{p1_team[p1_current_pokemon_id]['name']}은(는) 모래바람으로 인해 데미지를 입었다!")
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 16
                    if p1_team[p1_current_pokemon_id]["status"] == "Burn":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 화상 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 16
                    elif p1_team[p1_current_pokemon_id]["status"] == "Poison":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 독에 의한 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= p1_team[p1_current_pokemon_id]["max_status"][0] // 8
                    elif p1_team[p1_current_pokemon_id]["status"] == "SPoison":
                        print(f'{p1_team[p1_current_pokemon_id]["name"]}은(는) 독에 의한 데미지를 입었다!')
                        p1_team[p1_current_pokemon_id]['current_status'][0] -= (p1_team[p1_current_pokemon_id]["max_status"][0] // 16) * p1_team[p1_current_pokemon_id]["SPoison_cnt"]
                        p1_team[p1_current_pokemon_id]["SPoison_cnt"] += 1
                    if p1_team[p1_current_pokemon_id]['current_status'][0] <= 0:
                        p1_team[p1_current_pokemon_id]['current_status'][0] = 0
                        print(f"{p1_team[p1_current_pokemon_id]['name']}은(는) 기절했다!")
                    if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current < 2:
                        ca = 1
                        while ca:
                            a, idx, ca = choose_pokemon(1, p1_team, p1_current_pokemon_id)
                        p1_current_pokemon_id = idx
                        p1_team[p1_current_pokemon_id]['current_status'][0] = p1_team[p1_current_pokemon_id]["current_status"][0]
                        wait_for_enter("battle_turn", f"2P 다음 포켓몬: {p1_team[p1_current_pokemon_id]['name']}")
                        p1_fainted_flag = 1
                        p1_current+=1
                    if p1_team[p1_current_pokemon_id]['current_status'][0] == 0 and p1_current >= 2:
                        print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                        print("플레이어 2 승!")
                        exit()
                    if p1_team[p1_current_pokemon_id]['ability']=='가속' and p1_team[p1_current_pokemon_id]['turn']>=1:
                        p1_team[p1_current_pokemon_id]['rank'][4]=min(6,p1_team[p1_current_pokemon_id]['rank'][4]+1)
            if p1_current >= 3:
                print("플레이어 1의 포켓몬이 더 이상 남지 않았습니다")
                print("플레이어 2 승!")
                exit()
            elif p2_current >= 3:
                print("플레이어 2의 포켓몬이 더 이상 남지 않았습니다")
                print("플레이어 1 승!")
                exit()
            weather_timer=max(0,weather_timer - 1)
            if weather_timer == 0:
                weather=None
            trick_room_timer=max(0,trick_room_timer - 1)
            if trick_room_timer == 0:
                trick_room=None
            p1_reflect_timer=max(0,p1_reflect_timer - 1)
            if p1_reflect_timer == 0:
                p1_reflect=False
            p2_reflect_timer=max(0,p2_reflect_timer - 1)
            if p2_reflect_timer == 0:
                p2_reflect=False
            p1_l_screen_timer=max(0,p1_l_screen_timer - 1)
            if p1_l_screen_timer == 0:
                p1_l_screen=False
            p2_l_screen_timer=max(0,p2_l_screen_timer - 1)
            if p2_l_screen_timer == 0:
                p2_l_screen=False
            p1_team[p1_current_pokemon_id]['protect']=False
            p2_team[p2_current_pokemon_id]['protect']=False
    if state == "select_pokemon": draw_select_screen()
    elif state == "iv_setting": draw_iv_setting()
    elif state == "ev_setting": draw_ev_setting()
    elif state == "nature_up_setting": draw_nature_up_select()
    elif state == "nature_down_setting": draw_nature_down_select()
    elif state == "move_select": draw_move_select()
    elif state == "item_select": draw_item_select()
    elif state == "ability_select": draw_ability_select()
    elif state == "team_preview": draw_team_preview()
    elif state == "battle_select_1": draw_battle_select(team_1, "1P")
    elif state == "battle_select_2": draw_battle_select(team_2, "2P")
    elif state == "battle_ready": draw_battle_ready()
    elif state == "battle": draw_battle_screen()

    pygame.display.flip()
    clock.tick(30)
