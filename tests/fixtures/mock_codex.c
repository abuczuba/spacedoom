#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <limits.h>
int main(int argc, char **argv) {
    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));
    FILE *f = fopen(getenv("CDEV_TEST_LOG"), "a");
    if (!f) return 78;
    fprintf(f, "%s", cwd);
    for (int i=1; i<argc; ++i) fprintf(f, "\t%s", argv[i]);
    fprintf(f, "\n"); fclose(f);
    const char *mode = argc>1 && strcmp(argv[1],"resume")==0 ?
        (argc>2 && strcmp(argv[2],"--last")==0 ? "last" : "pinned") : "fresh";
    const char *fail = getenv("CDEV_TEST_FAIL");
    if (fail && strcmp(fail,mode)==0) return 23;
    if (fail && strcmp(fail,"late-pinned")==0 && strcmp(mode,"pinned")==0) { sleep(1); return 24; }
    for (;;) pause();
}
