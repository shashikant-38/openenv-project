from server.my_env_environment import MyEnvironment
from models import MyAction

env = MyEnvironment()
obs = env.reset(episode_id="episode-001", seed=42)
print("reset obs:", obs)

obs, reward, done, info = env.step(MyAction.FLAG)
print("step:", reward, done, info)
env.close()

