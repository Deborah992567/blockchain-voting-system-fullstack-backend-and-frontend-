// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ElectionVoting {

    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    address public admin;
    bool public isActive;

    mapping(address => bool) public hasVoted;
    mapping(uint256 => Candidate) public candidates;
    uint256 public candidatesCount;

    event VoteCast(address indexed voter, uint256 candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Admin only");
        _;
    }

    modifier electionActive() {
        require(isActive, "Election not active");
        _;
    }

    constructor(string[] memory candidateNames) {
        admin = msg.sender;

        for (uint256 i = 0; i < candidateNames.length; i++) {
            candidates[i] = Candidate({
                id: i,
                name: candidateNames[i],
                voteCount: 0
            });
            candidatesCount++;
        }
    }

    function startElection() external onlyAdmin {
        isActive = true;
    }

    function endElection() external onlyAdmin {
        isActive = false;
    }

    function vote(uint256 candidateId) external electionActive {
        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId < candidatesCount, "Invalid candidate");

        hasVoted[msg.sender] = true;
        candidates[candidateId].voteCount += 1;

        emit VoteCast(msg.sender, candidateId);
    }

    function getCandidate(uint256 candidateId)
        external
        view
        returns (string memory name, uint256 voteCount)
    {
        require(candidateId < candidatesCount, "Invalid candidate");
        Candidate memory c = candidates[candidateId];
        return (c.name, c.voteCount);
    }
}
