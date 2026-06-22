#!/bin/bash
# Agrégation MongoDB : collection tweets → users_aggregated
# Usage : bash scripts/aggregated.sh
# Prérequis : MongoDB local démarré, tweets importés via scripts/import_local.sh
# Export CSV : python Export_CSV.py

set -euo pipefail

DB_NAME="${DB_NAME:-database_local}"
MONGO_URI="${MONGO_URI:-mongodb://localhost:27017}"

if ! command -v mongosh &> /dev/null; then
  echo "mongosh introuvable"
  exit 1
fi

if ! mongosh --quiet --eval "db.runCommand({ ping: 1 })" &> /dev/null; then
  echo "MongoDB local non démarré"
  exit 1
fi

echo "Agrégation tweets → users_aggregated (base : ${DB_NAME})..."

mongosh "${MONGO_URI}/${DB_NAME}" --quiet <<'MONGOEOF'
db.tweets.aggregate([

  /* 1. Nettoyage + enrichissement par tweet */
  {
    $addFields: {
      is_retweet_flag: {
        $cond: [
          { $ifNull: ["$retweeted_status", false] },
          1,
          0
        ]
      },
      tweet_length: {
        $cond: [
          { $ifNull: ["$text", false] },
          { $strLenCP: "$text" },
          0
        ]
      },
      hashtags_count: { $size: { $ifNull: ["$entities.hashtags", []] } },
      urls_count: { $size: { $ifNull: ["$entities.urls", []] } },
      mentions_count: { $size: { $ifNull: ["$entities.user_mentions", []] } },
      tweet_date: {
        $dateFromString: {
          dateString: "$created_at"
        }
      }
    }
  },

  /* 2. Filtrage de sécurité */
  {
    $match: {
      "user.id": { $exists: true },
      tweet_date: { $ne: null }
    }
  },

  /* 3. Agrégation par utilisateur (user.id uniquement) */
  {
    $group: {
      _id: "$user.id",
      screen_name: { $first: "$user.screen_name" },
      verified: { $first: "$user.verified" },
      profile_lang: { $first: "$user.lang" },
      default_profile_image: { $first: "$user.default_profile_image" },
      followers_count: { $first: "$user.followers_count" },
      friends_count: { $first: "$user.friends_count" },
      nb_tweets: { $sum: 1 },
      nb_retweets: { $sum: "$is_retweet_flag" },
      avg_tweet_length: { $avg: "$tweet_length" },
      avg_hashtags: { $avg: "$hashtags_count" },
      avg_urls: { $avg: "$urls_count" },
      avg_mentions: { $avg: "$mentions_count" },
      avg_favorites: {
        $avg: { $ifNull: ["$favorite_count", 0] }
      },
      avg_retweet_count: {
        $avg: { $ifNull: ["$retweet_count", 0] }
      },
      first_tweet_date: { $min: "$tweet_date" },
      last_tweet_date: { $max: "$tweet_date" },
      active_days_set: {
        $addToSet: {
          $dateToString: {
            format: "%Y-%m-%d",
            date: "$tweet_date"
          }
        }
      }
    }
  },

  /* 4. Calculs finaux robustes */
  {
    $addFields: {
      active_days: { $size: "$active_days_set" },
      retweet_ratio: {
        $cond: [
          { $eq: ["$nb_tweets", 0] },
          0,
          { $divide: ["$nb_retweets", "$nb_tweets"] }
        ]
      },
      followers_friends_ratio: {
        $cond: [
          { $eq: ["$friends_count", 0] },
          "$followers_count",
          { $divide: ["$followers_count", "$friends_count"] }
        ]
      },
      tweet_frequency: {
        $cond: [
          { $lte: ["$active_days", 0] },
          0,
          { $divide: ["$nb_tweets", "$active_days"] }
        ]
      }
    }
  },

  /* 5. Projection finale (dataset ML-ready, 21 colonnes) */
  {
    $project: {
      _id: 0,
      user_id: "$_id",
      screen_name: 1,
      verified: 1,
      profile_lang: 1,
      default_profile_image: 1,
      followers_count: 1,
      friends_count: 1,
      followers_friends_ratio: 1,
      nb_tweets: 1,
      nb_retweets: 1,
      retweet_ratio: 1,
      avg_tweet_length: 1,
      avg_hashtags: 1,
      avg_urls: 1,
      avg_mentions: 1,
      avg_favorites: 1,
      avg_retweet_count: 1,
      first_tweet_date: 1,
      last_tweet_date: 1,
      active_days: 1,
      tweet_frequency: 1
    }
  },

  /* 6. Écriture dans la collection finale */
  {
    $out: "users_aggregated"
  }

])
MONGOEOF

echo "Agrégation terminée → collection users_aggregated"
echo "Export CSV : python Export_CSV.py"
