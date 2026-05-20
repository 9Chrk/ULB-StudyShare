"""Services métier liés aux statistiques globales."""

from typing import Optional

from core.db.manager import DBManager
from core.repository.statistics_repository import get_average_resumes_per_user
from core.repository.statistics_repository import get_best_rated_resumes_by_course
from core.repository.statistics_repository import get_courses_with_most_resumes
from core.repository.statistics_repository import get_most_bought_cosmetics
from core.repository.statistics_repository import get_top_users_by_points
from core.repository.statistics_repository import get_users_spending_more_than_available
from core.repository.statistics_repository import get_users_with_at_least_n_courses
from core.repository.statistics_repository import get_users_with_no_resumes


def get_statistics_data(user_id: Optional[int]) -> dict:
    """Renvoie toutes les statistiques demandées par le guide."""
    if not user_id:
        return {
            "top_users": [],
            "multi_course_users": [],
            "top_courses": [],
            "best_rated_resumes": [],
            "users_without_resumes": [],
            "most_bought_cosmetics": [],
            "overspending_users": [],
            "average_resumes_per_user": None,
        }

    with DBManager() as cursor:
        return {
            "top_users": get_top_users_by_points(cursor, 10),
            "multi_course_users": get_users_with_at_least_n_courses(cursor, 3),
            "top_courses": get_courses_with_most_resumes(cursor),
            "best_rated_resumes": get_best_rated_resumes_by_course(cursor),
            "users_without_resumes": get_users_with_no_resumes(cursor),
            "most_bought_cosmetics": get_most_bought_cosmetics(cursor),
            "overspending_users": get_users_spending_more_than_available(cursor),
            "average_resumes_per_user": get_average_resumes_per_user(cursor),
        }