#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>

struct msg {
	int i;
	char str[100];
} msg;

int main(void)
{
	setbuf(stdout, NULL);
	key_t key;
	int size, shmflg;
	int shmid, cmd;
	struct shmid_ds* buf;
	char* shmaddr;
	struct msg *segadr,*chdadr;
	int i, stat;

	static int statInt = 1;

	/* Create shm*/
	key = getpid();
	shmflg = IPC_CREAT | 0770; /*2. shmflg wasn't being set correctly by using shmflg |= ...*/
	/*printf("%X\n", shmflg);*/
	/*printf("%X\n", IPC_CREAT | 0770);*/
	shmid = shmget(key, sizeof(msg), shmflg);
	fprintf(stdout, "In parent: shmid =  %d\n", shmid);
	printf("shmget errno %s\n", strerror(errno));

	/* attach */
	segadr = (struct msg*)shmat(shmid, 0, 0);
	printf("shmat errno %s\n",strerror(errno)); /*1. segadr seems to be invalid - let's check errno*/


	/* copy*/
	segadr->i = 10;
	sprintf((char*)segadr->str,"A message from parent %d\n", getpid());
	/* new proc*/
	if (fork() == 0) { /* Is child*/
		printf("In Child: statInt %d\n", statInt);
		shmid = shmget(key, sizeof(msg), 0);
		fprintf(stdout, "In child: shmid = %d\n", shmid);
		chdadr = (struct msg *)shmat(shmid, 0, 0);
		printf("In Child: shmat errno %s\n",strerror(errno)); /* 3. Added errno debug, seems ok */
		fprintf(stdout, "This is child %d, gets %s\n", getpid(), chdadr->str); /* 4. We don't want to simply print chdadr, but rather the string */
		sprintf((char*)chdadr->str, "A message from child\n");
		printf("In Child: We've written a message back\n");
		if (shmdt(chdadr) == -1) {
			perror("Child - detach");
		}
		sleep(1);
		printf("In Child: statInt %d\n", statInt);
	}
	else { /* Is parent*/
		statInt = 2;
		printf("In Parent: We just changed statInt to %d\n", statInt);
		wait(&stat); //This will wait for the child to die
		fprintf(stdout, "In parent: segadr = %s\n", segadr->str); /* 4, so we need to do that here as well*/
		//system("ipcs");
		cmd = IPC_RMID;
		if (shmctl(shmid, cmd, buf) == -1) {
			perror("Parent - remove");

		}
	}
	return 0;
}
