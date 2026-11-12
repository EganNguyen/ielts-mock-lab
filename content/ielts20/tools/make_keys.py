#!/usr/bin/env python3
"""Transcribed answer keys for IELTS 20 Academic (keys are printed inline)."""
import json
from pathlib import Path

L = {
 "1": {
  "1": ["fish"], "2": ["roof"], "3": ["Spanish"], "4": ["vegetarians"],
  "5": ["Audley"], "6": ["hotel"], "7": ["reviews"], "8": ["local"],
  "9": ["30", "thirty"], "10": ["average"],
  "11": ["A"], "12": ["B"], "13": ["C"], "14": ["A"], "15": ["B"], "16": ["C"],
  "17": ["A", "E"], "18": ["A", "E"], "19": ["C", "E"], "20": ["C", "E"],
  "21": ["C", "E"], "22": ["C", "E"], "23": ["A", "C"], "24": ["A", "C"],
  "25": ["A", "B"], "26": ["A", "B"],
  "27": ["A"], "28": ["B"], "29": ["A"], "30": ["C"],
  "31": ["factories"], "32": ["dead"], "33": ["whale"], "34": ["apartments"],
  "35": ["park"], "36": ["art"], "37": ["beaches"], "38": ["ferry"],
  "39": ["bikes"], "40": ["drone"],
 },
 "2": {
  "1": ["break"], "2": ["time"], "3": ["shower"], "4": ["money"],
  "5": ["memory"], "6": ["lifting"], "7": ["fall"], "8": ["taxi"],
  "9": ["insurance"], "10": ["stress"],
  "11": ["D"], "12": ["I"], "13": ["H"], "14": ["E"], "15": ["A"], "16": ["B"],
  "17": ["B"], "18": ["A"], "19": ["B"], "20": ["A"],
  "21": ["D"], "22": ["G"], "23": ["B"], "24": ["A"], "25": ["E"],
  "26": ["C"], "27": ["A"], "28": ["A"], "29": ["B"], "30": ["C"],
  "31": ["photos", "photographs", "pictures"], "32": ["vegan"],
  "33": ["chefs", "cooks"], "34": ["journalists", "reporters"],
  "35": ["health"], "36": ["coffee"], "37": ["environment"],
  "38": ["reputation"], "39": ["price", "cost"], "40": ["soil"],
 },
 "3": {
  "1": ["239", "two hundred thirty-nine", "two hundred and thirty-nine"],
  "2": ["modern"], "3": ["lamp"], "4": ["Aaron"], "5": ["damage"],
  "6": ["electronic"], "7": ["insurance"], "8": ["space"], "9": ["app"],
  "10": ["exchanges"],
  "11": ["B"], "12": ["A"], "13": ["A"], "14": ["C"], "15": ["B"], "16": ["C"],
  "17": ["B"], "18": ["A"], "19": ["G"], "20": ["E"],
  "21": ["B"], "22": ["A"], "23": ["C"], "24": ["A"], "25": ["C"], "26": ["B"],
  "27": ["F"], "28": ["E"], "29": ["B"], "30": ["D"],
  "31": ["adaptation"], "32": ["cognitive"], "33": ["desks"], "34": ["taps"],
  "35": ["blue"], "36": ["voice"], "37": ["pregnant"], "38": ["shoulders"],
  "39": ["police"], "40": ["temperature"],
 },
 "4": {
  "1": ["Kings", "King's"], "2": ["125", "one hundred and twenty-five"],
  "3": ["walking"], "4": ["boat"], "5": ["Tuesday"], "6": ["space"],
  "7": ["vegetarian"], "8": ["2.30", "two thirty"], "9": ["75", "seventy-five"],
  "10": ["port"],
  "11": ["B", "C"], "12": ["B", "C"], "13": ["A", "C"], "14": ["A", "C"],
  "15": ["D"], "16": ["F"], "17": ["B"], "18": ["H"], "19": ["C"], "20": ["G"],
  "21": ["C", "E"], "22": ["C", "E"], "23": ["A", "C"], "24": ["A", "C"],
  "25": ["C"], "26": ["A"], "27": ["A"], "28": ["B"], "29": ["B"], "30": ["C"],
  "31": ["rats"], "32": ["snakes"], "33": ["tourism"], "34": ["traffic"],
  "35": ["rain"], "36": ["poison"], "37": ["building"], "38": ["dog"],
  "39": ["noise"], "40": ["combination"],
 },
}

R = {
 "1": {
  "1": ["FALSE"], "2": ["FALSE"], "3": ["FALSE"], "4": ["NOT GIVEN"],
  "5": ["TRUE"], "6": ["TRUE"],
  "7": ["Bulbs"], "8": ["Soil"], "9": ["feathers"], "10": ["Deer"],
  "11": ["1980"], "12": ["Funding"], "13": ["stakeholders"],
  "14": ["C"], "15": ["G"], "16": ["B"], "17": ["E"], "18": ["C"],
  "19": ["B"], "20": ["A"], "21": ["B"], "22": ["C"], "23": ["A"],
  "24": ["oak"], "25": ["flooring"], "26": ["keel"],
  "27": ["C"], "28": ["A"], "29": ["D"], "30": ["C"],
  "31": ["B"], "32": ["G"], "33": ["F"], "34": ["E"], "35": ["D"],
  "36": ["YES"], "37": ["NOT GIVEN"], "38": ["NO"], "39": ["YES"], "40": ["YES"],
 },
 "2": {
  "1": ["tail"], "2": ["flippers"], "3": ["hair"], "4": ["seagrasses"],
  "5": ["lips"], "6": ["buoyancy"],
  "7": ["TRUE"], "8": ["NOT GIVEN"], "9": ["FALSE"], "10": ["NOT GIVEN"],
  "11": ["TRUE"], "12": ["NOT GIVEN"], "13": ["TRUE"],
  "14": ["B"], "15": ["F"], "16": ["B"], "17": ["laziness"], "18": ["anxious"],
  "19": ["threats"], "20": ["exams"], "21": ["perfectionists"], "22": ["guilt"],
  "23": ["A", "C"], "24": ["A", "C"], "25": ["A", "E"], "26": ["A", "E"],
  "27": ["NO"], "28": ["YES"], "29": ["NOT GIVEN"], "30": ["NO"],
  "31": ["NOT GIVEN"], "32": ["YES"],
  "33": ["F"], "34": ["D"], "35": ["H"], "36": ["B"], "37": ["G"],
  "38": ["B"], "39": ["D"], "40": ["C"],
 },
 "3": {
  "1": ["potatoes"], "2": ["butter"], "3": ["meat"], "4": ["crystals"],
  "5": ["cellophane"], "6": ["tin"], "7": ["refrigerator"],
  "8": ["NOT GIVEN"], "9": ["TRUE"], "10": ["FALSE"], "11": ["TRUE"],
  "12": ["FALSE"], "13": ["NOT GIVEN"],
  "14": ["v"], "15": ["ii"], "16": ["iv"], "17": ["vii"], "18": ["iii"], "19": ["vi"],
  "20": ["C", "E"], "21": ["C", "E"], "22": ["B", "D"], "23": ["B", "D"],
  "24": ["tentacles"], "25": ["protection"], "26": ["colour"],
  "27": ["A"], "28": ["C"], "29": ["B"], "30": ["A"], "31": ["B"],
  "32": ["A"], "33": ["C"],
  "34": ["C"], "35": ["B"], "36": ["D"], "37": ["B"], "38": ["C"], "39": ["B"], "40": ["C"],
 },
 "4": {
  "1": ["teacher"], "2": ["charcoal"], "3": ["skyscrapers"], "4": ["flowers"],
  "5": ["bones"], "6": ["landscape"], "7": ["rivers"],
  "8": ["FALSE"], "9": ["TRUE"], "10": ["FALSE"], "11": ["TRUE"],
  "12": ["NOT GIVEN"], "13": ["NOT GIVEN"],
  "14": ["C"], "15": ["A"], "16": ["D"], "17": ["F"],
  "18": ["pumps"], "19": ["dams"], "20": ["float"], "21": ["crops"], "22": ["trees"],
  "23": ["B"], "24": ["E"], "25": ["A"], "26": ["C"],
  "27": ["D"], "28": ["G"], "29": ["B"], "30": ["C"], "31": ["B"],
  "32": ["D"], "33": ["E"], "34": ["B"], "35": ["C"], "36": ["A"],
  "37": ["jackals"], "38": ["diseases"], "39": ["food"], "40": ["foxes"],
 },
}

out = {test: {"listening": L[test], "reading": R[test]} for test in L}
Path("meta/keys.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
for test in out:
    for skill in ("listening", "reading"):
        assert sorted(int(k) for k in out[test][skill]) == list(range(1, 41)), (test, skill)
print("keys ok: 4 tests x 40 + 40")
