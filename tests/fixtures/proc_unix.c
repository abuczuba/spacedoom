/* Read-only macOS socket metadata for explicit, same-account test/peer PIDs. */
#include <libproc.h>
#include <sys/proc_info.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void string(const char *value, size_t maximum) {
    putchar('"');
    for (size_t i=0; i<maximum && value[i]; ++i) {
        unsigned char c=(unsigned char)value[i];
        if (c=='"' || c=='\\') printf("\\%c", c);
        else if (c<32 || c>=127) printf("\\u%04x", c);
        else putchar(c);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc<2 || argc>17) return 2;
    puts("["); int comma=0;
    for (int arg=1; arg<argc; ++arg) {
        char *end=NULL; long number=strtol(argv[arg], &end, 10);
        if (!end || *end || number<=1 || number>INT32_MAX) return 2;
        int pid=(int)number; struct proc_bsdinfo owner;
        if (proc_pidinfo(pid, PROC_PIDTBSDINFO, 0, &owner, sizeof owner)!=sizeof owner || owner.pbi_uid!=getuid()) return 3;
        int size=proc_pidinfo(pid, PROC_PIDLISTFDS, 0, NULL, 0);
        if (size<=0 || size>1024*1024) return 4;
        size+=32*(int)sizeof(struct proc_fdinfo);
        struct proc_fdinfo *files=calloc(1, (size_t)size);
        if (!files) return 4;
        int count=proc_pidinfo(pid, PROC_PIDLISTFDS, 0, files, size);
        if (count<0) { free(files); return 4; }
        for (int i=0; i<count/(int)sizeof(*files); ++i) {
            if (files[i].proc_fdtype!=PROX_FDTYPE_SOCKET) continue;
            struct socket_fdinfo item;
            if (proc_pidfdinfo(pid, files[i].proc_fd, PROC_PIDFDSOCKETINFO, &item, sizeof item)!=sizeof item) continue;
            if (item.psi.soi_family!=AF_UNIX || item.psi.soi_kind!=SOCKINFO_UN) continue;
            struct un_sockinfo *peer=&item.psi.soi_proto.pri_un;
            printf("%s{\"pid\":%d,\"fd\":%d,\"socket\":\"%llx\",\"pcb\":\"%llx\",\"peer_socket\":\"%llx\",\"peer_pcb\":\"%llx\",\"state\":%d,\"bound\":",
                   comma?",\n":"", pid, files[i].proc_fd,
                   (unsigned long long)item.psi.soi_so, (unsigned long long)item.psi.soi_pcb,
                   (unsigned long long)peer->unsi_conn_so, (unsigned long long)peer->unsi_conn_pcb,
                   item.psi.soi_state);
            string(peer->unsi_addr.ua_sun.sun_path, sizeof peer->unsi_addr.ua_sun.sun_path);
            printf(",\"connected_to\":");
            string(peer->unsi_caddr.ua_sun.sun_path, sizeof peer->unsi_caddr.ua_sun.sun_path);
            putchar('}'); comma=1;
        }
        free(files);
    }
    puts("\n]"); return 0;
}
