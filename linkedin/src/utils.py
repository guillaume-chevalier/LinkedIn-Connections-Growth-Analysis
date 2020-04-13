import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

FIGSIZE = (17, 5)
FONT = {"family": "sans-serif", "weight": "normal", "size": 16}
tds = "#17b78c"
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


def plot_cumsum_by_gender(df):
    cs_males = df[df["males"]].added.cumsum()
    cs_females = df[~df["males"]].added.cumsum()

    fig, ax = plt.subplots(figsize=FIGSIZE)

    plt.plot(cs_males.index, cs_males.values, c=tds, alpha=0.5, label="Males")
    plt.plot(cs_females.index, cs_females.values, c=tds, label="Females")

    plt.title(
        "LinkedIn connections evolution (cumulated) by gender", fontdict=FONT, y=1.2
    )
    plt.ylabel("Nb connections", fontdict=FONT)

    ax.set_frame_on(False)
    plt.grid(True)
    plt.legend(prop={"size": FONT["size"]})
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


def plot_violins_by_gender(df):
    females = violins_prep(df[~df.males][["added"]])
    females = females.assign(gender="Females")

    males = violins_prep(df[df.males][["added"]])
    males = males.assign(gender="Males")

    violins_gender = pd.concat([males, females])

    fig, ax = plt.subplots(figsize=(20, 8))

    ax = sns.violinplot(
        x="dow_str",
        y="added",
        hue="gender",
        data=violins_gender,
        split=True,
        alpha=0.5,
        color=tds,
        cut=0,
        ax=ax,
    )

    plt.title(
        "LinkedIn connections distribution per day of week per gender",
        fontdict=FONT,
        y=1.2,
    )
    plt.xlabel("Week day", fontdict=FONT)
    plt.ylabel("Nb daily connections", fontdict=FONT)
    plt.legend(prop={"size": FONT["size"]})

    ax.set_frame_on(False)
    plt.grid(True)
    plt.show()


def plot_bar_name(df):
    males = df[df.males].first_name.unique()
    fnames = df.first_name.value_counts().head(30)
    names = fnames.index.values
    fnames = fnames.reset_index()

    fig, ax = plt.subplots(figsize=FIGSIZE)
    mask_males = fnames["index"].isin(males)

    plt.bar(
        x=fnames[mask_males].index,
        height=fnames[mask_males].first_name,
        color=tds,
        alpha=0.5,
        label="Male",
    )
    plt.bar(
        x=fnames[~mask_males].index,
        height=fnames[~mask_males].first_name,
        color=tds,
        label="Female",
    )

    plt.title("First Names distribution", fontdict=FONT, y=1.2)
    plt.xticks(
        fnames.index,
        fnames["index"].str.capitalize(),
        rotation=65,
        ha="center",
        size=FONT["size"],
    )

    plt.ylabel("Nb occurences", fontdict=FONT)
    plt.yticks([0, 5, 10, 15, 20])
    ax.set_frame_on(False)
    plt.grid(True)
    plt.legend(prop={"size": FONT["size"]})

    plt.show()
