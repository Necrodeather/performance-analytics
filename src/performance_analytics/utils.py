from statistics import mean

from src.performance_analytics.domain.schemas import ServiceStatistic
from src.performance_analytics.private.models import PathModel


async def generate_path(path: PathModel) -> ServiceStatistic:
    statistics = [statistic.response_time for statistic in path.statistic]

    result = {
        "path": path.path,
        "average": int(mean(statistics)),
        "min": min(statistics),
        "max": max(statistics),
    }
    return ServiceStatistic.parse_obj(result)