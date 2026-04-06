CREATE TABLE Meetings (
    mID INT PRIMARY KEY,
    mDate DATE,
    location VARCHAR(50)
);

CREATE TABLE MeetingParticipants (
    pID INT,
    mID INT,
    risk INT CHECK (risk IN (0, 1)),
    PRIMARY KEY (pID, mID),
    FOREIGN KEY (mID) REFERENCES Meetings(mID)
);

CREATE TABLE Observers (
    oID INT PRIMARY KEY,
    favLocation VARCHAR(50)
);

CREATE TABLE Observations (
    oID INT,
    mID INT,
    pID INT,
    method VARCHAR(50),
    cLevel INT CHECK (cLevel BETWEEN 1 AND 100),
    PRIMARY KEY (oID, mID, pID),
    FOREIGN KEY (oID) REFERENCES Observers,
    FOREIGN KEY (pID, mID) REFERENCES MeetingParticipants(pID, mID)
);

