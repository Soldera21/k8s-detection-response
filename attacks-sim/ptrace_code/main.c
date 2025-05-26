#include <stdio.h>
#include <sys/ptrace.h>
#include <errno.h>

int main() {
    long ret = ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    if (ret == -1) {
        perror("ptrace");
        return 1;
    }

    printf("ptrace succeeded\n");
    return 0;
}
