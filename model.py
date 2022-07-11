import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    mean_absolute_error,
    mean_squared_log_error,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def Main():
    df_movie = pd.read_csv("files/data/movies_metadata_prepared_cleaned.csv", sep=";", engine="python")

    data = df_movie[
        [
            "belongs_to_collection",
            "original_title",
            "overview",
            "production_companies",
            "cast",
            "crew",
        ]
    ]

    # settings that you use for count vectorizer will go here
    tfidf_vectorizer = TfidfVectorizer(use_idf=True)

    x = data.copy()

    # construct the column transfomer
    column_transformer = ColumnTransformer(
        [
            ("tfidf_belongs_to_collection", tfidf_vectorizer, "belongs_to_collection"),
            ("tfidf_original_title", tfidf_vectorizer, "original_title"),
            ("tfidf_overview", tfidf_vectorizer, "overview"),
            ("tfidf_production_companies", tfidf_vectorizer, "production_companies"),
            ("tfidf_cast", tfidf_vectorizer, "cast"),
            ("tfidf_crew", tfidf_vectorizer, "crew"),
        ]
    )

    y = df_movie["vote_average"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=28)

    # -------------Ridge regression-------------
    ridg_reg = Ridge(alpha=10)

    print("-------------Ridge regression-------------\n")

    ridg_pipe = Pipeline([("tfidf", column_transformer), ("regression", ridg_reg)])

    ridg_pipe.fit(x_train, y_train)
    y_pred = ridg_pipe.predict(x_test)

    # The average squared difference between the estimated values and the actual value
    print(f"Mean squared error: {round(mean_squared_error(y_test, y_pred), 2)}")
    # The quadratic mean of these differences
    print(
        f"Root mean squared error: {round(mean_squared_error(y_test, y_pred, squared=False), 2)}"
    )
    print(f"Mean absolute error: {round(mean_absolute_error(y_test, y_pred))}")
    # The measure of the ratio between the true and predicted values.
    print(f"Mean squared log error: {round(mean_squared_log_error(y_test, y_pred), 2)}")
    # The coefficient of determination: 1 is perfect prediction
    print(f"Coefficient of determination: {round(r2_score(y_test, y_pred), 2)}")


if __name__ == "__main__":
    Main()
