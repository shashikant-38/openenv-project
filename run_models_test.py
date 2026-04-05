from models import MyAction, MyObservation

print(MyAction.ALLOW)
print(MyObservation(text="hi", toxicity_score=0.1, level="low"))

