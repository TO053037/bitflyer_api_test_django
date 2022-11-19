attraction_dic = {0: "", 1: "", 2: "スプラッシュマウンテン", 3: "プーさんのハニーハント", 4: "ビッグサンダーマウンテン", 5: "スペース・マウンテン",
                  6: "バス・ライトイヤーのアストロブラスター", 7: "モンスターズ・インクライド&ゴーシーク!", 8: "空飛ぶダンボ", 9: "ピータパン空の旅", 10: "ホーンテッドマンション",
                  11: "ピノキオの冒険旅行", 12: "白雪姫と七人のこびと", 13: "イッツ・ア・スモールワールド", 14: "", 15: "キャッスルカルーセル",
                  16: "ミッキーのフィルハーマジック", 17: "シンデレラのフェアリーテイル・ホール", 18: "スターツアーズ", 19: "スティッチ・エンカウンター", 20: "オムニバス",
                  21: "カリブの海賊", 22: "ジャングルクルーズ", 23: "ウエスタンリバー鉄道", 24: "", 25: "ウエスタンランド・シューティングギャラリー",
                  26: "カントリーベア・シアター", 27: "トムソーヤ島いかだ", 28: "ブーバーブラザーズのカヌー探検", 29: "スイスファミリー・ツリーハウス",
                  30: "ガジェットのゴーコースター", 31: "ロジャーラビットのカートゥーンスピン", 32: "グーフィーのペイント&プレイハウス", 33: "ミニーの家", 34: "ドナルドのボート",
                  35: "チップとデールのツリーハウス", }


def open_txt_file(file_path: str) -> str:
    f = open(file_path, 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data


if __name__ == '__main__':
    open_txt_file('./attractions_to/to_オムニバス.txt')
    num_attractions = 36
    distances_list = [[0 for _ in range(num_attractions)] for _ in range(num_attractions)]
    for i in range(num_attractions):
        attraction_i_name = attraction_dic[i]
        try:
            print(attraction_i_name)
            attractions_meter_data = open_txt_file('./attractions_meter/meter_{}.txt'.format(attraction_i_name)).split('\n')
            print(attractions_meter_data)
        except:
            continue
        for j in range(i + 1, num_attractions):
            attraction_j_name = attraction_dic[j]
            try:
                data = open_txt_file('./attractions_to/to_{}.txt'.format(attraction_j_name))
            except:
                continue
            for index, attraction_name in enumerate(data.split('\n')):
                if attraction_name == attraction_i_name and index < 39:
                    # distances_list[i][j] = attractions_meter_data[i]
                    # distances_list[j][i] = attractions_meter_data[i]
                    break

    # for dis in distances_list:
    #     print(dis)
