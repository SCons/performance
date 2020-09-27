/*

   Usage: spawn_test [#processes to create]

   Default is the current maximum of 32000 processes...

 Inspired by Trevor Highland (http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/),
 this little program spawns single processes in quick succession. 
 By allocating more and more memory at the same time, the runtimes for the single
 process calls seem to grow.
 Checking the output of "strace -o out.txt -r -f -s 256 spawn_test", the method
 wait() in the Kernel appears to be responsible for this behaviour.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

/* Activates the counting of machine instructions via ptrace().
 All code and comments for the following USE_PTRACE parts were
 copied from http://www.tldp.org/LDP/LGNET/81/sandeep.html .
*/
#define USE_PTRACE 0

#if USE_PTRACE == 1
#include <signal.h>
#include <syscall.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#endif

/* the maximum number of cycles (=processes to create) possible */
#define MAXCYCLES 32000
/* length of a single "dummy" signature (total_mem = SIGLEN*cycles) */
#define SIGLEN 20000

/* set to 0 or 1, 0=simple sleep, 1=exec */
#define USE_EXECUTE 1

/* set to 0 or 1, 0=allocate memory while spawning processes, 
                  1=pre-allocate memory before the main loop */
#define PRE_ALLOCATE_MEMORY 1
/* set to 0 or 1, 0=pre-allocate mem in single chunks of length SIGLEN
                  1=pre-allocate memory in one large block (cycles*SIGLEN) */
#define SINGLE_MEMORY_BLOCK 1

int main(int argc, char **argv)
{
    int cnt = 0;             /* simple counter for the current cycle */
    int cycles = MAXCYCLES;  /* number of cycles (=processes to create) */
    char echo_arg[100];      /* current argument for the echo command/process */
    char *m_list[MAXCYCLES]; /* list where we hold the allocated "dummy" signatures */
    pid_t child_pid;         /* pid of created child process */
    int child_status;        /* gets the child's status for the wait() */
#if USE_PTRACE == 1
    long long counter = 0;   /*  machine instruction counter */
#endif

    /* try to read the number of cycles from the command line */
    if (argc > 1) {
        cycles = atoi(argv[1]);
        if (cycles > MAXCYCLES) {
            cycles = MAXCYCLES;
            printf("Warning: setting number of cycles to internal maximum of %d!", MAXCYCLES);
        }
    }

#if PRE_ALLOCATE_MEMORY == 1
    printf("Allocating memory...\n");
#if SINGLE_MEMORY_BLOCK == 0
    for (; cnt < cycles; ++cnt) {
        /* get a new piece of memory, as if we'd be collecting build infos */
        m_list[cnt] = malloc(SIGLEN*sizeof(char));
        if (m_list[cnt] == NULL) {
            printf("No more memory left at %d...exiting.\n", cnt+1);
            exit(1);
        }
    }
#else
    m_list[0] = (char *) malloc(cycles*SIGLEN*sizeof(char));
    if (m_list[0] == NULL) {
        printf("No more memory left for pre-allocating all memory...exiting.\n");
        exit(1);
    }
#endif

#endif

    /* create processes and continually allocate memory */
    printf("Starting %d cycles...\n", cycles);
    for (cnt = 0; cnt < cycles; ++cnt) {
        sprintf(echo_arg, "%d/%d (%.2f%%)", cnt, cycles, ((double) cnt)*100.0/((double) cycles));

        printf("%s\n", echo_arg);
        child_pid = fork();
        if (child_pid == 0) {
            /* This is done by the child process. */
#if USE_PTRACE == 1
            ptrace(PTRACE_TRACEME, 0, 0, 0);
#endif
#if USE_EXECUTE == 1
            execlp("echo", echo_arg, NULL);

            /* If execlp returns, it must have failed. */
            printf("Unknown command\n");
#else
            sleep(0.01);
#endif
            exit(0);
        } else {
           /* This is run by the parent.  Wait for the child
              to terminate. */
#if USE_PTRACE == 1
            wait(&child_status); 
            /*   
             *   parent waits for child to stop at next 
             *   instruction (execl()) 
             */
            while (child_status == 1407 ) {
                    counter++;
                    if (ptrace(PTRACE_SINGLESTEP, child_pid, 0, 0) != 0)
                            perror("ptrace");
                    /* 
                     *   switch to singlestep tracing and 
                     *   release child
                     *   if unable call error.
                     */
                    wait(&child_status);
                    /*   wait for next instruction to complete  */
            }
            /*
             * continue to stop, wait and release until
             * the child is finished; wait_val != 1407
             * Low=0177L and High=05 (SIGTRAP)
             */
#else
           while (wait(&child_status) != child_pid)
               ;
#endif

        }
#if PRE_ALLOCATE_MEMORY == 0
        /* get a new piece of memory, as if we'd be collecting build infos */
        m_list[cnt] = malloc(SIGLEN*sizeof(char));
        strcpy(m_list[cnt], echo_arg);
#else
#if SINGLE_MEMORY_BLOCK == 0
        strcpy(m_list[cnt], echo_arg);
#else
        strcpy(m_list[0] + cnt*SIGLEN, echo_arg);
#endif
#endif
    }

    printf("Done.\n");
#if USE_PTRACE == 1
    printf("Number of machine instructions : %lld\n", counter);
#endif
}

