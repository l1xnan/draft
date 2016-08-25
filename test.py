def score_staging(course):
    condition = [
        {"$match": {"score.math.state": 0}},
        {'$group': {
            '_id': {"grade_id": "$grade_id"},
            'avg': {'$avg': "$score." + course + ".final"},
            'total': {'$sum': 1},
            's1': {'$sum': {'$cond': [{
                '$and': [
                    {"$lt": ["$score." + course + ".final", {
                        '$multiply': ["$score." + course + ".full", 0.6]}]},
                    {"$gte": ["$score." + course + ".final", {
                        '$multiply': ["$score." + course + ".full", 0]}]}
                ]
            }, 1, 0]}},
            's2': {'$sum': {'$cond': [{
                '$and': [
                    {"$lt": ["$score." + course + ".final", {
                            '$multiply': ["$score." + course + ".full", 0.8]}]},
                    {"$gte": ["$score." + course + ".final", {
                        '$multiply': ["$score." + course + ".full", 0.6]}]}
                ]
            }, 1, 0]}},
            's3': {'$sum': {'$cond': [{
                '$and': [
                    {"$lt": ["$score." + course + ".final", {
                            '$multiply': ["$score." + course + ".full", 0.9]}]},
                    {"$gte": ["$score." + course + ".final", {
                        '$multiply': ["$score." + course + ".full", 0.8]}]}
                ]
            }, 1, 0]}},
            's4': {'$sum': {'$cond': [{
                '$and': [
                    {"$lte": ["$score." + course + ".final", {
                            '$multiply': ["$score." + course + ".full", 1.0]}]},
                    {"$gte": ["$score." + course + ".final", {
                        '$multiply': ["$score." + course + ".full", 0.9]}]}
                ]
            }, 1, 0]}},
        }
        },
        {"$sort": {"_id": 1}}]
    result = db.finalexam.aggregate(condition)
    return list(result)
