import json

try:
    # Import modules
    import rpc
    import time
    from ReadWriteMemory import ReadWriteMemory
    from ReadWriteMemory import ReadWriteMemoryError

    procNameTable = {
        "동방요요몽": 7,
        "동방영야초": 8,
        "동방풍신록": 10,
        "동방지령전": 11,
        "동방성련선": 12,
        "동방신령묘": 13,
        "동방휘침성": 14,
        "동방감주전": 15,
        "동방천공장": 16,
        "동방귀형수": 17
    }

    procNameInput = input("RPC에 띄울 게임은? ")
    if procNameInput not in procNameTable.keys():
        print("지원하지 않는 게임이거나 존재하지 않음")
        input()
        exit(0)
    else:
        rwm = ReadWriteMemory()
        gozaMarisa = ""
        if len(str(procNameTable[procNameInput])) == 1:
            gozaMarisa = f'0{str(procNameTable[procNameInput])}'
        else:
            gozaMarisa = str(procNameTable[procNameInput])
        try:
            process = rwm.get_process_by_name(f'th{gozaMarisa}.exe')
            process.open()
        except ReadWriteMemoryError as error:
            print(error)
            input()
            exit(0)

        # Connect to Discord
        cid = input('RPC Client ID: ')
        rpc_obj = rpc.DiscordIpcClient.for_platform(cid)  # Send the client ID to the rpc module
        if True:  # procNameTable[procNameInput] in range(10, 13):
            ptrTable = json.load(open("data/memtable/fuu.json", "r"))
            print(ptrTable)

        # Update RPC every 15 seconds
        start_time = time.time()
        diff = [
            "이지",
            "노멀",
            "하드",
            "루나틱"
        ]
        while True:
            g = f"잔기 {process.read(ptrTable['life'])}개 (조각 {process.read(ptrTable['lifePiece'])}개)"
            # , 스펠카드 {process.read(ptrTable['bomb'])}개 (조각 {process.read(ptrTable['bomb'])}개)
            t = f"{process.read(ptrTable['score']) * 10}점 / 난이도 {diff[process.read(ptrTable['difficulty'])]}"
            # , 영력 {list(str(process.read(ptrTable['power'])))[0]}.{list(str(process.read(ptrTable['power'])))[1]}{
            # list(str(process.read(ptrTable['power'])))[2]}
            activity = {
                "state": g,
                "details": t,
                "timestamps": {
                    "start": start_time
                },
                "assets": {
                    "small_text": "동방성련선",
                    "small_image": "th12",
                    "large_text": "동방성련선",
                    "large_image": "th12"
                }
            }
            try:
                rpc_obj.set_activity(activity)
            except OSError as e:
                print(e)
                print(activity)
            time.sleep(15)

# Custom KeyboardInterrupt message
except KeyboardInterrupt:
    print('\nProgram stopped using Ctrl+C.')
