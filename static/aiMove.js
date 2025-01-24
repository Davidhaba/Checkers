function makeAIMove() {
    const currentCheckers = document.querySelectorAll(`.checker.${currentPlayer}`);
    if (!currentCheckers.length > 0) return;

    if (allowTouchChange || !selectedChecker) {
        checker = getRandomChecker(currentCheckers);
        if (checker) selectedChecker = checker;
    }
    if (selectedChecker) {
        const moves = getAvailableMoves(selectedChecker);
        availableMoves = moves.availableMoves || [];
        captureMoves = moves.captureMoves || [];
    }
    if (!mandatoryCapture || (captureMoves && captureMoves.length === 0)) {
        if (selectedChecker && ((captureMoves && captureMoves.length > 0) || (availableMoves && availableMoves.length > 0))) {
            const targetCell = (captureMoves && captureMoves.length > 0)
                ? captureMoves[Math.floor(Math.random() * captureMoves.length)]
                : availableMoves[Math.floor(Math.random() * availableMoves.length)];

            if (targetCell) performMove(targetCell);
        }
    } else {
        if (captureMoves && captureMoves.length > 0) {
            const targetCell = captureMoves[Math.floor(Math.random() * captureMoves.length)];
            if (targetCell) performMove(targetCell);
        }
    }
}
function getRandomChecker(checkers) {
    const allCheckers = Array.from(checkers);
    let candidateChecker = null;
    while (allCheckers.length > 0) {
        const checker = allCheckers.splice(Math.floor(Math.random() * allCheckers.length), 1)[0];
        if (checker) {
            const moves = getAvailableMoves(checker);
            const availableMoves = moves.availableMoves || [];
            const captureMoves = moves.captureMoves || [];
            if (mandatoryCapture && captureMoves.length > 0) {
                return checker;
            }
            if (availableMoves.length > 0 || captureMoves.length > 0) {
                candidateChecker = checker;
            }
        }
    }
    return candidateChecker;
}

function checkAiTurn() {
    if (gameSettings.gameMode === 'single' && currentPlayer === 'black') {
        setTimeout(makeAIMove, 500);
    }
}
