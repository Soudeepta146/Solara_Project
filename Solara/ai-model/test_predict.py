import json
from src.model.predict import predict

result = predict(22.57, 88.36, "EV")


print(json.dumps(result, indent=2))

