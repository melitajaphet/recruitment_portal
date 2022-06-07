import json


def score(entities):
    with open('job_profile.json', mode = 'r') as reader:
        profile = json.load(reader)

    score = 0
    for key in profile.keys():
        if key in entities.keys():
            profile_values = set(profile[key])
            entity_values = set(entities[key])
            common = profile_values.intersection(entity_values)
            if len(common) != 0:
                score += len(common)
    return score