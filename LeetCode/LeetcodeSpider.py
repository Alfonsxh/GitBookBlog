"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Spider.py
@time: 2019/8/2 上午7:46
@version: v1.0 
"""
import os
import json
import requests


def leetcode_crawl():
    diff_dict = {
        1: "Easy",
        2: "Medium",
        3: "Hard"
    }
    leetcode_url = "https://leetcode.com/api/problems/all/"
    leetcode_json_file = "leetcode.json"

    contents = json.loads(requests.get(url=leetcode_url).content)

    if os.path.isfile(leetcode_json_file):
        with open(leetcode_json_file, "r") as fr:
            questions_dict = {int(key): value for key, value in json.load(fr).items()}
    else:
        questions_dict = dict()

    for q in contents.get("stat_status_pairs", list()):
        question_id = q.get("stat", dict()).get("frontend_question_id")
        if question_id is None:
            continue

        question_name = q.get("stat", dict()).get("question__title")
        question_url = "https://leetcode.com/problems/{}/description/".format(q.get("stat", dict()).get("question__title_slug", ""))
        question_diff = diff_dict.get(q.get("difficulty", dict()).get("level"), "unknow")
        question_paid = q.get("paid_only")

        if questions_dict.get(question_id, dict()).get("sol") or question_id in questions_dict:
            continue

        questions_dict.update({question_id: dict(name=question_name, url=question_url, lock=question_paid, diff=question_diff, sol=dict())})

    questions_dict = {k: v for k, v in sorted(questions_dict.items(), key=lambda a: a[0])}
    with open(leetcode_json_file, "w") as f:
        f.write(json.dumps(questions_dict, indent=4))

    return questions_dict


def markdown_write(leetcode_dict: dict):
    total_question = len(leetcode_dict)
    solve_question = len([1 for q in leetcode_dict.values() if q.get("sol")])

    with open("README.md", "w") as f:
        f.write("|#|Title|Difficulty|Solution({solve}/{total})|\n|:---:|:---|:---|:---|\n".format(solve=solve_question, total=total_question))
        for leetcode_number, leetcode_info in leetcode_dict.items():
            f.write("|{number}|[{title}]({url}){lock}|{diff}|{sol}|\n".format(number=leetcode_number,
                                                                              title=leetcode_info["name"],
                                                                              url=leetcode_info["url"],
                                                                              lock=":lock:" if leetcode_info["lock"] else "",
                                                                              diff=leetcode_info["diff"],
                                                                              sol=", ".join(
                                                                                  ["[{t}]({u})".format(t=sol_type, u=sol_url) for sol_type, sol_url in
                                                                                   leetcode_info["sol"].items()])))
    pass


if __name__ == '__main__':
    markdown_write(leetcode_crawl())
    pass
