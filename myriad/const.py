import signal


# Signals
SIGUSR1 = 30
SIGUSR2 = 31
signalLookup = {
    signal.SIGHUP: "terminal line hangup",
    signal.SIGINT: "interrupt program",
    signal.SIGQUIT: "quit program",
    signal.SIGILL: "illegal instruction",
    signal.SIGTRAP: "trace trap",
    signal.SIGABRT: "abort program (formerly SIGIOT)",
    signal.SIGEMT: "emulate instruction executed",
    signal.SIGFPE: "floating-point exception",
    signal.SIGKILL: "kill program",
    signal.SIGBUS: "bus error",
    signal.SIGSEGV: "segmentation violation",
    signal.SIGSYS: "non-existent system call invoked",
    signal.SIGPIPE: "write on a pipe with no reader",
    signal.SIGALRM: "real-time timer expired",
    signal.SIGTERM: "software termination signal",
    signal.SIGURG: "urgent condition present on socket",
    signal.SIGSTOP: "stop (cannot be caught or ignored)",
    signal.SIGTSTP: "stop signal generated from keyboard",
    signal.SIGCONT: "continue after stop",
    signal.SIGCHLD: "child status has changed",
    signal.SIGTTIN: "background read attempted from control terminal",
    signal.SIGTTOU: "background write attempted to control terminal",
    signal.SIGIO: "I/O is possible on a descriptor (see fcntl(2))",
    signal.SIGXCPU: "cpu time limit exceeded (see setrlimit(2))",
    signal.SIGXFSZ: "file size limit exceeded (see setrlimit(2))",
    signal.SIGVTALRM: "virtual time alarm (see setitimer(2))",
    signal.SIGPROF: "profiling timer alarm (see setitimer(2))",
    signal.SIGWINCH: "Window size change",
    signal.SIGINFO: "status request from keyboard",
    SIGUSR1: "User defined signal 1",
    SIGUSR2: "User defined signal 2",
}

# Exit codes
OK = 0
GENERAL_ERROR = 1
ILLEGAL_COMMAND = 126
COMMAND_NOT_FOUND = 127
INVALID_EXIT = 128
INTERRUPTED = 128 + signal.SIGINT
ABORTED = 128 + signal.SIGABRT
CONTROL_D = 160

# Options
GAME_TYPE = "gametype"
STORY_DIR = "storydir"
STORY_FILE = "storyfile"
STORY_MODULE = "storymodule"
BANNER_FILE = "bannerfile"

# Subcommands
KEYGEN = "keygen"
SHELL = "shell"
STOP = "stop"

# Game types
LOCAL = "local"
SINGLE = "singleplayer"
MULTI = "multiplayer"


# Human perceptual average distance to horizon on Earth, in miles; this is
# taken as the unit size of a tile. To provide some reference, a small town of
# 3000 people can easily fit in 2 square miles (that's about 1300 residential
# buildings). So a single tile of 3.1 miles x 3.1 miles will provide plenty of
# space for a small town.
# 
# A large city can be in the neighborhood of 500 square miles (e.g., New York
# City) with a population density of 28,000 people per square mile (which would
# be 84000 people per tile). A city the size of NYC would require about 150
# tiles, a grid of 10 by 15 tiles.
#
# The next step up in order of magnitude, 100 by 100 tiles, would be about the
# size of the state of Michigan (the 11th largest state in the US).
# 
# As a further extreme, a continent the size of North America (about 3 times
# larger than the surface area of Australia) would be 1000 by 1000 tiles.
#
# And finally, the Earth itself has a total of 316944047 square miles (land and
# sea) which would be about 102240015 tiles, or a grid of 10002 by 10222 tiles.
horizonDistance = 3.1


# Directions
N = 0
S = 1
E = 2
W = 3
NE = 4
SE = 5
SW = 6
NW = 7
# "C" stands for "center"
C = 8
# "U" stands for "up"
U = 9
# "D" stands for "down"
D = 10
directions = [N, S, E, W, NE, SE, SW, NW, C, U, D]
