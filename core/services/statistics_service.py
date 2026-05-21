"""Services metier lies aux statistiques globales."""

from typing import Optional

from core.db.manager import DBManager
import core.models.statistics as models
import core.repository.statistics_repository as repository


def get_statistics_data(user_id: Optional[int]) -> models.StatisticsData:
    """Renvoie toutes les statistiques demandees par le guide."""
    if not user_id:
        return models.StatisticsData(
            top_users=[],
            multi_course_users=[],
            top_courses=[],
            best_rated_resumes=[],
            users_without_resumes=[],
            most_bought_cosmetics=[],
            overspending_users=[],
            average_resumes_per_user=None,
        )

    with DBManager() as cursor:
        top_users = [
            models.TopUserStat(username=row[0], points=row[1], level=row[2])
            for row in repository.get_top_users_by_points(cursor, 10)
        ]

        multi_course_users = [
            models.MultiCourseUserStat(
                username=row[0], course_count=row[1], resume_count=row[2]
            )
            for row in repository.get_users_with_at_least_n_courses(cursor, 3)
        ]

        top_courses = [
            models.TopCourseStat(code=row[0], name=row[1], resume_count=row[2])
            for row in repository.get_courses_with_most_resumes(cursor)
        ]

        best_rated_resumes = [
            models.BestRatedResumeStat(
                course_code=row[0],
                course_name=row[1],
                resume_title=row[2],
                average_rating=float(row[3]),
            )
            for row in repository.get_best_rated_resumes_by_course(cursor)
        ]

        users_without_resumes = [
            models.UserWithoutResumeStat(username=row[0], email=row[1], points=row[2])
            for row in repository.get_users_with_no_resumes(cursor)
        ]

        most_bought_cosmetics = [
            models.MostBoughtCosmeticStat(
                item_id=row[0],
                name=row[1],
                description=row[2],
                price_points=row[3],
                purchase_count=row[4],
            )
            for row in repository.get_most_bought_cosmetics(cursor)
        ]

        overspending_users = [
            models.OverspendingUserStat(
                username=row[0], points=row[1], total_spent=row[2], excess_spent=row[3]
            )
            for row in repository.get_users_spending_more_than_available(cursor)
        ]

        return models.StatisticsData(
            top_users=top_users,
            multi_course_users=multi_course_users,
            top_courses=top_courses,
            best_rated_resumes=best_rated_resumes,
            users_without_resumes=users_without_resumes,
            most_bought_cosmetics=most_bought_cosmetics,
            overspending_users=overspending_users,
            average_resumes_per_user=repository.get_average_resumes_per_user(cursor),
        )
