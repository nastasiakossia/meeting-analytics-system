# ANALYSIS QUERIES

ANALYSIS_Q1 = """
SELECT M.pid, COUNT(*) AS meeting_count, SUM(M.risk) AS risky_meeting_count
FROM MeetingParticipants M
    INNER JOIN CoveredLowRiskParticipants С
        ON С.pid = M.pid
    INNER JOIN BusyMeetings B
        ON B.mid = M.mid
GROUP BY M.pid
HAVING COUNT(*) >= 5
ORDER BY meeting_count DESC, M.pid ASC
    """

ANALYSIS_Q2 = """           
SELECT DISTINCT O.mid, O.oid
FROM Observations O 
    INNER JOIN MeetingMaxConfidence M
        ON O.mid = M.mid
WHERE O.cLevel = M.max_confidence
    """

ANALYSIS_Q3 = """           
SELECT M.location, COUNT(DISTINCT M.mid) AS meeting_count
FROM Meetings M
    INNER JOIN NonPreferredMeetings N
        ON M.mid = N.mid
    INNER JOIN EfficientObservers E
        ON E.mid = M.mid
GROUP BY M.location
    """


# PARTICIPANTS QUERIES
GET_LOCATIONS = """
SELECT DISTINCT location
FROM Meetings
ORDER BY location;
"""

GET_PARTICIPANTS = """
SELECT DISTINCT pid
FROM MeetingParticipants
ORDER BY pid;
"""

GET_MEETINGS = """
SELECT mid
FROM Meetings
ORDER BY mid;
"""

GET_OBSERVERS = """
SELECT oid
FROM Observers
ORDER BY oid;
"""

GET_METHODS = """
SELECT DISTINCT method
FROM Observations
WHERE method IS NOT NULL
ORDER BY method;
"""

FIND_PARTICIPANTS_BY_LOCATION = """
SELECT DISTINCT MP.pid
FROM MeetingParticipants MP
JOIN Meetings M ON M.mid = MP.mid
WHERE M.location = %s
  AND MP.risk = 1
  AND EXISTS (
      SELECT 1
      FROM Observations O
      WHERE O.mid = MP.mid
        AND O.pid = MP.pid
  )
ORDER BY MP.pid;
"""

PARTICIPANT_STATS = """
SELECT
    (
        SELECT COUNT(DISTINCT O.oid)
        FROM Observations O
        WHERE O.pid = %s
    ) AS observer_count,
    (
        SELECT COUNT(DISTINCT M.mid)
        FROM MeetingParticipants M
        WHERE M.pid = %s
          AND NOT EXISTS (
              SELECT 1
              FROM Observations O2
              WHERE O2.mid = M.mid
                AND O2.pid = M.pid
          )
    ) AS meetings_without_observation,
    COALESCE(
        (
            SELECT TOP 1 O3.method
            FROM Observations O3
            WHERE O3.pid = %s
            GROUP BY O3.method
            ORDER BY COUNT(*) DESC, O3.method ASC
        ),
        'NA'
    ) AS top_observation_method;
"""

ADD_OBSERVATION_INSERT = """
INSERT INTO Observations (mid, oid, pid, method, cLevel)
VALUES (%s, %s, %s, %s, %s);
"""

CHECK_PARTICIPANT_IN_MEETING = """
SELECT 1
FROM MeetingParticipants
WHERE mid = %s AND pid = %s;
"""

CHECK_OBSERVATION_EXISTS = """
SELECT 1
FROM Observations
WHERE mid = %s AND pid = %s AND oid = %s;
"""

GET_OBSERVER_AVG_CONFIDENCE = """
SELECT AVG(CAST(cLevel AS FLOAT))
FROM Observations
WHERE oid = %s;
"""
