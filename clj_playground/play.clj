(ns play
  (:require [honey.sql :as sql]))


(sql/format {:select [:u.username]
             :from   [[:user :u]]
             :where  [:= :id 1]})
