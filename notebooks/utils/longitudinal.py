import pandas as pd

def summarize_longitudinal(df, date_col, id_col="subject_label"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    summary = (
        df.sort_values([id_col, date_col])
          .groupby(id_col)
          .agg(
              n_visits=(date_col, "nunique"),
              first_date=(date_col, "min"),
              last_date=(date_col, "max"),
          )
    )

    summary["followup_years"] = (
        summary["last_date"] - summary["first_date"]
    ).dt.days / 365.25

    long_ids = summary.index[summary["n_visits"] >= 2]
    df_long = df[df[id_col].isin(long_ids)].copy()

    stats = {
        "n_subjects": len(long_ids),
        "n_records": len(df_long),
        "mean_followup": summary.loc[long_ids, "followup_years"].mean(),
        "std_followup": summary.loc[long_ids, "followup_years"].std(),
    }

    return df_long, summary, stats