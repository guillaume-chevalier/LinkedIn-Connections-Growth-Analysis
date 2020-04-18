import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

FIGSIZE = (16, 9)
FONT = {"family": "Share Tech Mono", "weight": "normal", "size": 16}
tds = "#0073b1"
week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def plot_weekly_connection(df):
    weekly = df[["added"]].resample("W").sum()

    fig, ax = plt.subplots(figsize=FIGSIZE)

    plt.plot(weekly.index, weekly.added, c=tds)

    plt.title("LinkedIn connections evolution", fontdict=FONT, y=1.2)
    plt.ylabel("Nb weekly connections", fontdict=FONT)

    ax.set_frame_on(False)
    plt.grid(True)
    plt.show()


def plot_cumsum(df):
    cumsum = df.added.cumsum()

    fig, ax = plt.subplots(figsize=FIGSIZE)

    plt.plot(cumsum.index, cumsum.values, c=tds)

    plt.title("LinkedIn connections evolution (cumulated)", fontdict=FONT, y=1.2)
    plt.ylabel("Nb connections", fontdict=FONT)

    ax.set_frame_on(False)
    plt.grid(True)
    plt.show()


def violins_prep(tmp):
    tmp = tmp.resample("D").sum()
    tmp = tmp.assign(dow=tmp.index.dayofweek.values).sort_values("dow")
    return tmp.assign(dow_str=tmp.dow.apply(lambda d: week[d]))


def plot_violins(df):
    violins = violins_prep(df[["added"]])

    fig, ax = plt.subplots(figsize=(20, 8))
    ax = sns.violinplot(x="dow_str", y="added", data=violins, color=tds, cut=0, ax=ax)

    plt.title("LinkedIn connections distribution per day of week", fontdict=FONT, y=1.2)
    plt.xlabel("Week day", fontdict=FONT)
    plt.ylabel("Nb daily connections", fontdict=FONT)

    ax.set_frame_on(False)
    plt.grid(True)
    plt.show()


def plot_bar_column(df, col):
    fnames = df[col].value_counts().head(30)
    plot_fnames(fnames,col)


def plot_nlp_cv(df):
    tfidf = CountVectorizer(ngram_range=(1, 3), stop_words='english')
    cleaned_positions = list(df["Position"].fillna(""))
    res = tfidf.fit_transform(cleaned_positions)
    res = res.toarray().sum(axis=0)

    fnames = pd.DataFrame(
        list(sorted(zip(res, tfidf.get_feature_names())))[-30:],
        columns=["Position by Words Freq", "Words"]
    )[::-1] 
    plot_fnames(fnames, "Position by Words Freq", "Words")


def plot_fnames(fnames, col, index="index"):
    fnames = fnames.reset_index()

    fig, ax = plt.subplots(figsize=FIGSIZE)

    plt.bar(
        x=fnames.index,
        height=fnames[col],
        color=tds,
        alpha=0.5
    )

    plt.title("{} distribution".format(col), fontdict=FONT, y=1.2)
    plt.xticks(
        fnames.index,
        fnames[index].str.capitalize(),
        rotation=65,
        ha="right",
        size=FONT["size"],
    )

    plt.ylabel("Nb occurences", fontdict=FONT)
    plt.yticks()#[0, 5, 10, 15, 20])
    ax.set_frame_on(False)
    plt.grid(True)

    plt.show()

