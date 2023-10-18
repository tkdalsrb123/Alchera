import os, sys, logging, json, random
from tqdm import tqdm

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

purpose = [
"게이밍",
"그래픽 디자인",
"영상 편집",
"업무용",
"홈 엔터테인먼트",
"프로그래밍",
"학생용",
"서버 운용",
"3D 모델링",
"가정용 미디어 센터",
"가상 현실 (VR) 게임",
"머신 러닝 및 딥 러닝",
"사무실 업무용",
"음악 제작 및 편집",
"호스트 서버",
"브라우징 및 온라인 활동",
"사무실 업무용 소프트웨어 개발",
"클라우드 컴퓨팅",
"인공 지능 (AI) 개발",
"미디어 스트리밍"
]

itmes = [
"Dell XPS 13",
"HP Spectre x360",
"Lenovo ThinkPad X1 Carbon",
"Asus ZenBook Pro Duo",
"Acer Predator Helios 300",
"MSI GS66 Stealth",
"Apple MacBook Air",
"Microsoft Surface Laptop 4",
"Razer Blade 15",
"Alienware m15 R4",
"Gigabyte Aero 15 OLED",
"LG Gram 17",
"Huawei MateBook X Pro",
"Lenovo Legion Y740",
"Dell Alienware Area-51m",
"Asus ROG Zephyrus G14",
"HP Omen X",
"Acer Swift 7",
"Microsoft Surface Book 3",
"Apple MacBook Pro",
"Google Pixelbook Go",
"Samsung Galaxy Book S",
"LG Gram 14",
"Lenovo Yoga C940",
"Asus VivoBook S15",
"HP Envy 13",
"Dell Inspiron 14 2-in-1",
"Acer Chromebook Spin 13",
"MSI Prestige 14",
"Microsoft Surface Pro 7",
"Razer Blade Stealth 13",
"Alienware Aurora R11",
"HP Pavilion Gaming Desktop",
"Lenovo Legion Tower 5",
"Asus ROG Strix GA15",
"Acer Predator Orion 9000",
"MSI Trident 3 9SI-447US",
"Dell G5 Gaming Desktop",
"Apple Mac mini",
"Microsoft Surface Studio 2",
"Razer Tomahawk",
"Alienware Aurora Ryzen Edition",
"Gigabyte Aero 15 OLED XC",
"HP ZBook Fury G7",
"Asus ProArt StudioBook Pro 17",
"LG UltraFine 5K Display",
"Lenovo ThinkCentre M90n",
"Acer Aspire TC-895-UA92",
"MSI Cubi N",
"Dell Precision 755"]

cpu = [
"Intel i9-10900K",
"AMD Ryzen 9 5950X",
"Intel i7-10700",
"AMD Ryzen 7 5800X",
"Intel i5-10600K",
"AMD Ryzen 5 5600X",
"Intel i3-10100",
"AMD Ryzen 3 3300X",
"Intel Xeon E-2288G",
"AMD Threadripper 3990X",
"Intel Core i9-9900KS",
"AMD Ryzen 9 3950X",
"Intel Pentium Gold G6400",
"AMD Athlon 3000G",
"Intel Xeon W-2295",
"AMD EPYC 7742",
"Intel Core i7-9700K",
"AMD Ryzen 7 3700X",
"Intel Core i5-9400F",
"AMD Ryzen 5 3600"
]

cooler = [
"Cooler Master Hyper 212 RGB",
"NZXT Kraken X63",
"Noctua NH-D15",
"Corsair H100i RGB Platinum",
"be quiet! Dark Rock Pro 4",
"Arctic Freezer 34 eSports Duo",
"Cooler Master MasterLiquid ML240R",
"Deepcool Gammaxx 400",
"Scythe Mugen 5 Rev.B",
"Thermaltake Floe Riing RGB 360",
"Cooler Master Hyper 212 Black Edition",
"NZXT Kraken Z73",
"Noctua NH-U12A",
"Corsair iCUE H150i Elite Capellix",
"be quiet! Dark Rock 4",
"Arctic Liquid Freezer II 240",
"Cooler Master Hyper 212 RGB Black Edition",
"Deepcool Gammaxx GT BK",
"Scythe Fuma 2",
"Thermaltake Water 3.0 ARGB"
]

memory = [
"16GB DDR4 3200MHz",
"32GB DDR4 3600MHz",
"64GB DDR4 4000MHz",
"8GB DDR4 3000MHz",
"16GB DDR3 2400MHz",
"32GB DDR3 2666MHz",
"64GB DDR3 2800MHz",
"8GB DDR3 2133MHz",
"16GB DDR3 1866MHz",
"32GB DDR3 2133MHz",
"64GB DDR3 2400MHz",
"8GB DDR4 2133MHz",
"16GB DDR4 2400MHz",
"32GB DDR4 2800MHz",
"64GB DDR4 3000MHz",
"8GB DDR4 2666MHz",
"16GB DDR4 3000MHz",
"32GB DDR4 3200MHz",
"64GB DDR4 3600MHz",
"128GB DDR4 4000MHz"
]

mainbord = [
"ASUS ROG Strix Z490-E Gaming",
"MSI MPG B550 Gaming Edge WiFi",
"Gigabyte X570 Aorus Elite WiFi",
"ASRock B450M Steel Legend",
"ASUS TUF B450M-Plus Gaming",
"MSI B450 Tomahawk Max",
"Gigabyte B360 Aorus Gaming 3",
"ASRock H410M-HDV/M.2",
"ASUS Prime Z390-A",
"MSI Z390-A PRO",
"Gigabyte Z370P D3",
"ASRock H370M-ITX/ac",
"ASUS ROG Maximus XII Hero",
"MSI MPG B550I Gaming Edge WiFi",
"Gigabyte B550M DS3H",
"ASRock X570 Phantom Gaming 4",
"ASUS ROG Strix X570-E Gaming",
"MSI MEG Z490 Godlike",
"Gigabyte X299 Aorus Master",
"ASRock X399 Taichi"
]

graphic = [
"NVIDIA GeForce RTX 3080",
"AMD Radeon RX 6800 XT",
"NVIDIA GeForce GTX 1660 Ti",
"AMD Radeon RX 5700 XT",
"NVIDIA Quadro P5000",
"AMD Radeon RX 5500 XT",
"NVIDIA Tesla V100",
"AMD Radeon Pro WX 7100",
"NVIDIA GeForce GT 1030",
"AMD Radeon Pro WX 2100",
"NVIDIA Quadro RTX 5000",
"AMD Radeon Pro WX 5100",
"NVIDIA Titan RTX",
"AMD Radeon Pro WX 3100",
"NVIDIA Quadro P400",
"AMD Radeon RX 560",
"NVIDIA Tesla K80",
"AMD Radeon Pro WX 4100",
"NVIDIA Quadro P2000",
"AMD Radeon RX 580"
]

ssd = [
"Samsung 970 EVO Plus NVMe M.2 1TB",
"Crucial MX500 2.5 SATA III 1TB",
"Western Digital Black SN750 NVMe M.2 500GB",
"Kingston A2000 NVMe M.2 1TB",
"Samsung 860 EVO 2.5 SATA III 500GB",
"Crucial P1 NVMe M.2 1TB",
"Western Digital Blue 3D NAND 2.5 SATA III 1TB",
"Kingston UV500 2.5 SATA III 480GB",
"Samsung 970 PRO NVMe M.2 1TB",
"Crucial BX500 2.5 SATA III 240GB",
"Western Digital Green 2.5 SATA III 240GB",
"Kingston KC600 2.5 SATA III 512GB",
"Samsung 970 EVO NVMe M.2 500GB",
"Crucial MX300 2.5 SATA III 525GB",
"Western Digital Black SN750 NVMe M.2 1TB with Heatsink",
"Kingston KC2000 NVMe M.2 1TB",
"Samsung 860 QVO 2.5 SATA III 1TB",
"Crucial P5 NVMe M.2 1TB",
"Western Digital Blue 3D NAND 2.5 SATA III 500GB",
"Kingston KC2500 NVMe M.2 1TB"
]
Case = [
"NZXT H510i",
"Fractal Design Meshify C",
"Cooler Master MasterBox Q300L",
"Phanteks Eclipse P300A",
"Corsair iCUE 220T RGB Airflow",
"Lian Li Lancool II Mesh",
"NZXT H510 Compact ATX Mid-Tower",
"Fractal Design Define R6",
"Cooler Master MasterCase H500P Mesh",
"Phanteks Enthoo Pro M",
"Corsair Obsidian 500D RGB SE",
"Lian Li PC-O11 Dynamic",
"NZXT H710i",
"Fractal Design Define 7 Compact",
"Cooler Master Cosmos C700P",
"Phanteks Evolv X",
"Corsair Crystal 570X RGB",
"Lian Li PC-O11 Dynamic XL",
"NZXT H710i Matte Black/Red",
"Fractal Design Define 7"
]

power = [
"500W",
"600W",
"700W",
"800W",
"900W"
]

include = ['포함', '미포함']


def jsonTree(path):
    tree = {
        "사용용도": random.choice(purpose),
        "본체가격": f"{random.randrange(300000, 2500000)} 원",
        "모니터 포함 여부": random.choice(include),
        "CPU": random.choice(cpu),
        "CPU쿨러": random.choice(cooler),
        "메모리": random.choice(memory),
        "메인보드": random.choice(mainbord),
        "그래픽": random.choice(graphic),
        "SSD": random.choice(ssd),
        "케이스": random.choice(Case),
        "소비전력": random.choice(power),
        "가격": f"{random.randrange(300000, 2500000)} 원"
    }
    saveJson(tree, path)

if __name__ == '__main__':
    _, output_dir = sys.argv
    
    json_num = 2000 # json 출력 개수 설정
    for i in tqdm(range(json_num)):
        num = str(i).zfill(4)
        output_path = f"{output_dir}/{num}.json"
        jsonTree(output_path)
