from controllers import HealthController, IndexController

routes = [
    (r"/", IndexController),
    (r"/health", HealthController),
]
