DROP VIEW IF EXISTS dbo.BusyMeetings;
DROP VIEW IF EXISTS dbo.UnmonitoredParticipants;
DROP VIEW IF EXISTS dbo.VersatileObservers;
DROP VIEW IF EXISTS dbo.ComplexMeetings;
DROP VIEW IF EXISTS dbo.QualifiedComplexMeetings;
DROP VIEW IF EXISTS dbo.MeetingMaxConfidence;
DROP VIEW IF EXISTS dbo.LowConfidenceObservations;
DROP VIEW IF EXISTS dbo.EfficientObservers;
DROP VIEW IF EXISTS dbo.NonPreferredMeetings;
go

CREATE VIEW BusyMeetings AS
SELECT DISTINCT M1.mid
FROM Meetings M1
JOIN Meetings M2
  ON M1.mDate = M2.mDate
 AND M1.location = M2.location
 AND M1.mid <> M2.mid
WHERE EXISTS (
    SELECT MP.mid
    FROM MeetingParticipants MP
    WHERE MP.mid = M1.mid
    GROUP BY MP.mid
    HAVING COUNT(*) >= 5
)
GO

CREATE VIEW UnmonitoredParticipants AS
SELECT DISTINCT M.pid
FROM MeetingParticipants M
WHERE NOT EXISTS (
    SELECT M1.pid
    FROM MeetingParticipants M1
    WHERE M1.risk = 0
    AND M.pid = M1.pid
    AND NOT EXISTS(
        SELECT O1.pid, O1.mid
        FROM Observations O1
        WHERE O1.pid = M1.pid
        AND O1.mid = M1.mid
    )
)
GO


CREATE VIEW VersatileObservers AS
SELECT DISTINCT O1.oid
FROM Observations O1
WHERE NOT EXISTS(
    (SELECT DISTINCT M1.location
    FROM Meetings M1)
    EXCEPT
    (SELECT DISTINCT M2.location
    FROM Meetings M2 INNER JOIN Observations O2
        ON O2.mid = M2.mid
    WHERE O1.oid = O2.oid)
)
GO

CREATE VIEW ComplexMeetings AS
SELECT O.mid
FROM Observations O
GROUP BY O.mid
HAVING
    COUNT(DISTINCT O.oid) >= 3
    AND MIN(O.cLevel) >= 60
GO

CREATE VIEW QualifiedComplexMeetings AS
SELECT O.mid
FROM Observations O
INNER JOIN ComplexMeetings C
  ON C.mid = O.mid
INNER JOIN VersatileObservers V
  ON V.oid = O.oid
GROUP BY O.mid
HAVING COUNT(O.oid) >= 2
GO

CREATE VIEW MeetingMaxConfidence AS
SELECT Q.mid, MAX(O.cLevel) AS max_confidence
    FROM Observations O INNER JOIN QualifiedComplexMeetings Q
    ON O.mid = Q.mid
    GROUP BY Q.mid
GO

CREATE VIEW LowConfidenceObservations AS
SELECT O.mid, O.oid, O.pid
FROM Observations O INNER JOIN MeetingParticipants M
    ON O.pid = M.pid
    AND O.mid = M.mid
WHERE M.risk = 1
AND O.cLevel < (
    SELECT AVG(CAST(O1.cLevel AS FLOAT))
    FROM Observations O1
    WHERE O1.method = O.method
    AND O1.oid = O.oid
    )
GO

CREATE VIEW EfficientObservers AS
SELECT O.oid, O.mid
FROM Observations O
WHERE NOT EXISTS(
    SELECT L.mid
    FROM LowConfidenceObservations L
    WHERE O.mid = L.mid
    AND O.oid = L.oid
)
GROUP BY O.oid, O.mid
HAVING COUNT(*) >= 2
GO

CREATE VIEW NonPreferredMeetings AS
SELECT M.mid
FROM Meetings M
WHERE NOT EXISTS(
    SELECT 1
    FROM Observations O1 INNER JOIN Observers O
    ON O.oid = O1.oid
    WHERE O1.mid = M.mid
    AND M.location = O.favLocation
)
GO

