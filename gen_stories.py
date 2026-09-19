import json, os

# word key -> (surface, furigana, romaji, gloss, pos)
V = {
  # greetings/time
  "arigatou": ("ありがとう", "ありがとう", "arigatou", "thank you", "expression"),
  "sumimasen": ("すみません", "すみません", "sumimasen", "excuse me / sorry", "expression"),
  "hai": ("はい", "はい", "hai", "yes", "interjection"),
  "iie": ("いいえ", "いいえ", "iie", "no", "interjection"),
  "kyou": ("今日", "きょう", "kyou", "today", "noun"),
  "ashita": ("明日", "あした", "ashita", "tomorrow", "noun"),
  "kinou": ("昨日", "きのう", "kinou", "yesterday", "noun"),
  "maiasa": ("毎朝", "まいあさ", "maiasa", "every morning", "noun"),
  "jikan": ("時間", "じかん", "jikan", "time / hour", "noun"),
  "asa": ("朝", "あさ", "asa", "morning", "noun"),
  "yoru": ("夜", "よる", "yoru", "night", "noun"),
  # people
  "kodomo": ("子ども", "こども", "kodomo", "child", "noun"),
  "hito": ("人", "ひと", "hito", "person", "noun"),
  "tomodachi": ("友達", "ともだち", "tomodachi", "friend", "noun"),
  "kazoku": ("家族", "かぞく", "kazoku", "family", "noun"),
  "chichi": ("父", "ちち", "chichi", "father", "noun"),
  "haha": ("母", "はは", "haha", "mother", "noun"),
  "oniisan": ("お兄さん", "おにいさん", "onii-san", "older brother", "noun"),
  "oneesan": ("お姉さん", "おねえさん", "onee-san", "older sister", "noun"),
  "watashi": ("私", "わたし", "watashi", "I / me", "pronoun"),
  # body
  "kao": ("顔", "かお", "kao", "face", "noun"),
  "me": ("目", "め", "me", "eye", "noun"),
  "te": ("手", "て", "te", "hand", "noun"),
  "ashi": ("足", "あし", "ashi", "foot / leg", "noun"),
  "atama": ("頭", "あたま", "atama", "head", "noun"),
  # numbers
  "ichi": ("一", "いち", "ichi", "one", "number"),
  "futatsu": ("二つ", "ふたつ", "futatsu", "two (things)", "number"),
  # colors
  "akai": ("赤い", "あかい", "akai", "red", "adjective"),
  "aoi": ("青い", "あおい", "aoi", "blue", "adjective"),
  "shiroi": ("白い", "しろい", "shiroi", "white", "adjective"),
  "kuroi": ("黒い", "くろい", "kuroi", "black", "adjective"),
  # food
  "gohan": ("ご飯", "ごはん", "gohan", "meal / rice", "noun"),
  "pan": ("パン", "パン", "pan", "bread", "noun"),
  "mizu": ("水", "みず", "mizu", "water", "noun"),
  "ocha": ("お茶", "おちゃ", "ocha", "tea", "noun"),
  "kouhii": ("コーヒー", "コーヒー", "kouhii", "coffee", "noun"),
  "ringo": ("りんご", "りんご", "ringo", "apple", "noun"),
  "banana": ("バナナ", "バナナ", "banana", "banana", "noun"),
  # animals
  "inu": ("犬", "いぬ", "inu", "dog", "noun"),
  "neko": ("猫", "ねこ", "neko", "cat", "noun"),
  "tori": ("鳥", "とり", "tori", "bird", "noun"),
  "sakana": ("魚", "さかな", "sakana", "fish", "noun"),
  # transportation
  "densha": ("電車", "でんしゃ", "densha", "train", "noun"),
  "jitensha": ("自転車", "じてんしゃ", "jitensha", "bicycle", "noun"),
  # nature/weather
  "tenki": ("天気", "てんき", "tenki", "weather", "noun"),
  "ame": ("雨", "あめ", "ame", "rain", "noun"),
  "yama": ("山", "やま", "yama", "mountain", "noun"),
  "kawa": ("川", "かわ", "kawa", "river", "noun"),
  # places
  "ginkou": ("銀行", "ぎんこう", "ginkou", "bank", "noun"),
  "byouin": ("病院", "びょういん", "byouin", "hospital", "noun"),
  "toshokan": ("図書館", "としょかん", "toshokan", "library", "noun"),
  "suupaa": ("スーパー", "スーパー", "suupaa", "supermarket", "noun"),
  "gakkou": ("学校", "がっこう", "gakkou", "school", "noun"),
  "ie": ("家", "いえ", "ie", "house / home", "noun"),
  "kouen": ("公園", "こうえん", "kouen", "park", "noun"),
  # work/tech
  "kaisha": ("会社", "かいしゃ", "kaisha", "company", "noun"),
  "joushi": ("上司", "じょうし", "joushi", "boss", "noun"),
  "douryou": ("同僚", "どうりょう", "douryou", "colleague", "noun"),
  "miitingu": ("ミーティング", "ミーティング", "miitingu", "meeting", "noun"),
  "konpyuutaa": ("コンピューター", "コンピューター", "konpyuutaa", "computer", "noun"),
  "meeru": ("メール", "メール", "meeru", "email", "noun"),
  "denwa": ("電話", "でんわ", "denwa", "telephone", "noun"),
  "hon": ("本", "ほん", "hon", "book", "noun"),
  # verbs (polite forms as they appear in text)
  "taberu": ("食べます", "たべます", "tabemasu", "to eat", "verb"),
  "nomu": ("飲みます", "のみます", "nomimasu", "to drink", "verb"),
  "iku": ("行きます", "いきます", "ikimasu", "to go", "verb"),
  "kuru": ("来ます", "きます", "kimasu", "to come", "verb"),
  "miru": ("見ます", "みます", "mimasu", "to see / watch", "verb"),
  "yomu": ("読みます", "よみます", "yomimasu", "to read", "verb"),
  "kaku": ("書きます", "かきます", "kakimasu", "to write", "verb"),
  "hanasu": ("話します", "はなします", "hanashimasu", "to speak", "verb"),
  "yasumu": ("休みます", "やすみます", "yasumimasu", "to rest", "verb"),
  "tetsudau": ("手伝います", "てつだいます", "tetsudaimasu", "to help", "verb"),
  "hataraku": ("働きます", "はたらきます", "hatarakimasu", "to work", "verb"),
  "tsukau": ("使います", "つかいます", "tsukaimasu", "to use", "verb"),
  "kau": ("買います", "かいます", "kaimasu", "to buy", "verb"),
  "aru": ("あります", "あります", "arimasu", "there is (thing)", "verb"),
  "iru": ("います", "います", "imasu", "there is (living thing)", "verb"),
  "tsukareru": ("疲れます", "つかれます", "tsukaremasu", "to get tired", "verb"),
  # adjectives
  "ii": ("良い", "いい", "ii", "good", "adjective"),
  "warui": ("悪い", "わるい", "warui", "bad", "adjective"),
  "ookii": ("大きい", "おおきい", "ookii", "big", "adjective"),
  "chiisai": ("小さい", "ちいさい", "chiisai", "small", "adjective"),
  "takai": ("高い", "たかい", "takai", "high / expensive", "adjective"),
  "yasui": ("安い", "やすい", "yasui", "cheap", "adjective"),
  "atarashii": ("新しい", "あたらしい", "atarashii", "new", "adjective"),
  "furui": ("古い", "ふるい", "furui", "old", "adjective"),
  "omoshiroi": ("面白い", "おもしろい", "omoshiroi", "interesting", "adjective"),
  "isogashii": ("忙しい", "いそがしい", "isogashii", "busy", "adjective"),
  "taisetsu": ("大切", "たいせつ", "taisetsu", "important", "adjective"),
  "chikai": ("近い", "ちかい", "chikai", "near / close", "adjective"),
}

# grammar glue: particles, demonstratives, conjunctions - not part of the vocab list
P = {
  "wa": ("は", "は", "wa", "topic marker", "particle"),
  "ga_subj": ("が", "が", "ga", "subject marker", "particle"),
  "ga_but": ("が", "が", "ga", "but", "conjunction"),
  "wo": ("を", "を", "wo", "object marker", "particle"),
  "ni": ("に", "に", "ni", "to / at / in", "particle"),
  "de": ("で", "で", "de", "at / by means of", "particle"),
  "to": ("と", "と", "to", "and / with", "particle"),
  "no": ("の", "の", "no", "possessive marker", "particle"),
  "mo": ("も", "も", "mo", "also / too", "particle"),
  "kara": ("から", "から", "kara", "from", "particle"),
  "made": ("まで", "まで", "made", "until / to", "particle"),
  "desu": ("です", "です", "desu", "polite ending", "copula"),
  "sorekara": ("それから", "それから", "sorekara", "after that", "conjunction"),
  "kono": ("この", "この", "kono", "this (+noun)", "determiner"),
  "sore": ("それ", "それ", "sore", "that", "pronoun"),
  "arimasen": ("ありません", "ありません", "arimasen", "there isn't", "verb"),
}
MARU = ("。", "", "", "", "punct")
TOUTEN = ("、", "", "", "", "punct")

def tok(key):
    if key == "。":
        surface, furigana, romaji, gloss, pos = MARU
    elif key == "、":
        surface, furigana, romaji, gloss, pos = TOUTEN
    else:
        src = V.get(key) or P.get(key)
        if src is None:
            raise KeyError(key)
        surface, furigana, romaji, gloss, pos = src
    return {
        "surface": surface,
        "furigana": furigana,
        "romaji": romaji,
        "dictForm": surface,
        "pos": pos,
        "gloss": gloss,
    }

def make_story(id_, title, level, stage, keys, translation):
    return {
        "id": id_,
        "title": title,
        "level": level,
        "stage": stage,
        "tokens": [tok(k) for k in keys],
        "translation": translation,
    }

stories = []

# ---------- Stage 1: greetings, family, simple daily actions ----------
stories.append(make_story(
    "story-01", "私の一日", "n5", 1,
    ["watashi","wa","asa","gohan","wo","taberu","。",
     "sorekara","gakkou","ni","iku","。",
     "gakkou","de","tomodachi","to","hanasu","。",
     "tomodachi","wa","ii","hito","desu","。"],
    "I eat breakfast in the morning. After that, I go to school. I talk with my friend at school. My friend is a good person."
))
stories.append(make_story(
    "story-02", "家族", "n5", 1,
    ["watashi","no","kazoku","wa","chichi","to","haha","to","oniisan","desu","。",
     "haha","wa","ii","hito","desu","。",
     "kyou","wa","kazoku","to","gohan","wo","taberu","。"],
    "My family is my father, mother, and older brother. My mother is a good person. Today I eat a meal with my family."
))

# ---------- Stage 2: numbers, colors, body ----------
stories.append(make_story(
    "story-03", "赤いりんご", "n5", 2,
    ["sore","wa","watashi","no","te","desu","。",
     "te","de","akai","ringo","wo","taberu","。",
     "ringo","wa","futatsu","aru","。",
     "kuroi","neko","mo","iru","。"],
    "That is my hand. I eat a red apple with my hand. There are two apples. There is also a black cat."
))
stories.append(make_story(
    "story-04", "私の顔", "n5", 2,
    ["watashi","no","kao","ni","me","ga_subj","futatsu","aru","。",
     "atama","wa","chiisai","desu","。",
     "ashi","wa","ookii","desu","。"],
    "My face has two eyes. My head is small. My feet are big."
))

# ---------- Stage 3: food, animals, transportation ----------
stories.append(make_story(
    "story-05", "公園への道", "n5", 3,
    ["kyou","wa","densha","de","kouen","ni","iku","。",
     "kouen","de","inu","to","tori","wo","miru","。",
     "sakana","mo","iru","。",
     "kono","kouen","wa","omoshiroi","desu","。"],
    "Today I go to the park by train. I see a dog and a bird at the park. There is also fish. This park is interesting."
))
stories.append(make_story(
    "story-06", "朝ごはん", "n5", 3,
    ["maiasa","、","watashi","wa","pan","wo","taberu","。",
     "kouhii","mo","nomu","。",
     "ocha","mo","nomu","。",
     "banana","to","ringo","wa","yasui","desu","。"],
    "Every morning I eat bread. I also drink coffee. I also drink tea. Bananas and apples are cheap."
))

# ---------- Stage 4: nature, weather, places ----------
stories.append(make_story(
    "story-07", "山と川", "n5", 4,
    ["kono","yama","wa","takai","desu","。",
     "yama","no","chikai","kawa","ni","aru","。",
     "kyou","wa","tenki","ga_subj","ii","desu","。",
     "ame","wa","arimasen","。"],
    "This mountain is tall. There is a river near the mountain. Today the weather is good. There is no rain."
))
stories.append(make_story(
    "story-08", "図書館まで", "n5", 4,
    ["watashi","no","ie","kara","toshokan","made","iku","。",
     "toshokan","de","hon","wo","yomu","。",
     "sorekara","suupaa","de","gohan","wo","kau","。",
     "byouin","no","chikai","ginkou","ga_subj","aru","。"],
    "I go from my house to the library. I read a book at the library. After that, I buy a meal at the supermarket. There is a bank near the hospital."
))

# ---------- Stage 5: work, tech ----------
stories.append(make_story(
    "story-09", "会社の一日", "n5", 5,
    ["watashi","wa","kaisha","de","hataraku","。",
     "kyou","wa","joushi","to","douryou","to","miitingu","ga_subj","aru","。",
     "miitingu","wa","isogashii","desu","ga_but","taisetsu","desu","。",
     "kaisha","de","meeru","wo","kaku","。",
     "denwa","mo","tsukau","。"],
    "I work at the company. Today there is a meeting with my boss and colleague. The meeting is busy, but important. I write email at the company. I also use the phone."
))
stories.append(make_story(
    "story-10", "新しいコンピューター", "n5", 5,
    ["kaisha","no","konpyuutaa","wa","furui","desu","。",
     "atarashii","konpyuutaa","wa","takai","desu","。",
     "douryou","wa","atarashii","konpyuutaa","wo","tsukau","。",
     "watashi","wa","tsukareru","。",
     "yasumu","。"],
    "The company's computer is old. The new computer is expensive. My colleague uses the new computer. I get tired. I rest."
))

base = "/home/claude/jlpt-reader/src/data/n5"
for s in stories:
    stage_dir = os.path.join(base, f"stage-{s['stage']}")
    os.makedirs(stage_dir, exist_ok=True)
    path = os.path.join(stage_dir, f"{s['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print("wrote", path)
