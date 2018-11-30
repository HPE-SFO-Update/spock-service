import sched, time
from threading import Thread
from library.constants.Time import HOUR,DAY,WEEK
from library.util.MetaClasses import Singleton
from library.aws.FileSearch import SpockRetrieve
from library.util.SpockMap import SpockMap
from library.util.Tools import path_from_top_directory
from library.constants.Map import MAP_PATH


class SchedulerUpdateMap(object, metaclass=Singleton):
    __instance = None

    def __init__(self):
        if SchedulerUpdateMap.__instance is None:
            SchedulerUpdateMap.__instance = self
            self.scheduler = sched.scheduler(time.time, time.sleep)
        else:
            raise Exception("Use SchedulerUpdateMap.get_instance()")

    @staticmethod
    def get_instance():
        if SchedulerUpdateMap.__instance is None:
            SchedulerUpdateMap.__instance = SchedulerUpdateMap()
        return SchedulerUpdateMap.__instance

    @staticmethod
    def spock_update():
        SpockRetrieve.initialize()
        SpockRetrieve.download_map()
        SpockMap.open(path_from_top_directory(MAP_PATH))

    def setup_schedule(self):
        if self.scheduler.empty():
            self.scheduler.enter(1, 1, SchedulerUpdateMap.spock_update)
            self.scheduler.enter(DAY, 1, SchedulerUpdateMap.spock_update)
            self.scheduler.run()

    @staticmethod
    def spawn():
        if SchedulerUpdateMap.empty():
            Thread(target=SchedulerUpdateMap.get_instance().setup_schedule).start()

    @staticmethod
    def empty():
        return SchedulerUpdateMap.get_instance().scheduler.empty()


def check_spock_map(funct):
    """
    Decorator design for rest api. Updates spock map.
    :param funct: the function that is decorated
    :return: wrapper function
    """
    def wrapper(*args):
        """
        Wrapper function that updates spock map
        :param args: arguments of the function that is being decorated
        :return:
        """
        SchedulerUpdateMap.spawn()
        return funct(*args)
    return wrapper


if __name__ == "__main__":
    print(SchedulerUpdateMap.get_instance().empty())
    SchedulerUpdateMap.spawn()
    print(SchedulerUpdateMap.get_instance().empty())
    SchedulerUpdateMap.spawn()
    print(SchedulerUpdateMap.get_instance().empty())
    time.sleep(60*10)
    print(SchedulerUpdateMap.get_instance().empty())
