(ns play
  (:require
    [clojure.string :as str]
    [honey.sql :as sql]))


(sql/format {:select [:*]
             :from   [[:user :u]]
             :where  [:= :id 1]} {:quoted true})

(def x {:select [:*] :from [:table] :group-by [:foo :bar]})

(defn pythonify
  [x]
  (-> x
      (update-keys str)
      (update-vals (fn [v]
                     (cond
                       (map? v)
                       (pythonify v)

                       (coll? v)
                       (into [] (map str v))

                       :else
                       (str v))))))

;; format-dsl
;; format-clause

(defn format-value
  [v]
  (cond
    (coll? v)
    (format "[%s]" (str/join ", " (map pr-str v)))

    :else
    v))

(format-value ["1",2,3])


(defn pprint-py
  [x]
  (let [x (pythonify x)]
    (println "{")
    (doseq [[k v] x]
      (cond
        (map? v)
        (pprint-py v)

        (coll? v)
        (print
          (pr-str k)
          ":"
          (format-value v)
          ",")

        :else
        (print (format "%s: %s," (pr-str k) (pr-str v))))
      (println))
    (println "}")))

(pprint-py {:select [:*] :from [:table] :where [:= :id 1]})
