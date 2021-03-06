#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/file.h>
#include <fcntl.h>
#include <time.h>
#define TAM 256

char *DATA = "data.csv";
char *DATAGEN = "dataGen.csv";
char *LASTDATA = "lastData.csv";


char* strTruncByChar(char *str, char c);
char* strcut(char *str, int begin,int end);	

int main(int argc, char const *argv[])
{
	FILE* dataFile;
	FILE* lastData;
	FILE* dataGenFile = fopen(DATAGEN, "w");
	fclose(dataGenFile);
	char buffer[TAM];
	int fileHandler;

	while(1){
		
		dataFile = fopen(DATA, "r");

		//abre el archivo de datos dataGen en append
		dataGenFile = fopen(DATAGEN, "a");
		//lee la primera linea y no la guarda porque ya esta guardada
		fileHandler = fileno(dataGenFile);
		//obtiene exclusion mutua del archivo
		flock(fileHandler, LOCK_EX);
		fgets(buffer, TAM, dataFile);
		//libera exclusion mutua del archivo
		flock(fileHandler, LOCK_UN);
		fclose(dataGenFile);

		while(fgets(buffer, TAM, dataFile)){

			strcpy(buffer,strTruncByChar(buffer,'\n'));
			//abre el archivo de datos dataGen en append
			dataGenFile = fopen(DATAGEN, "a");
			//abre el archivo lastData en modo write
			lastData = fopen(LASTDATA, "w");	
			printf("%s\n", buffer);

			fileHandler = fileno(dataGenFile);
			//obtiene exclusion mutua del archivo
			flock(fileHandler,LOCK_EX);
			fprintf(dataGenFile, "%s\n", buffer);
			//libera exclusion mutua del archivo
			flock(fileHandler,LOCK_UN);

			fileHandler = fileno(lastData);
			//obtiene exclusion mutua del archivo
			flock(fileHandler,LOCK_EX);
			fprintf(lastData, "%s\n", buffer);
			//libera exclusion mutua del archivo
			flock(fileHandler,LOCK_UN);

			fclose(lastData);
			fclose(dataGenFile);
			sleep(1);
		}
		fclose(dataFile);
	}
	return 0;
}


char* strTruncByChar(char *str, char c){
	int len = strlen(str);
	int i;
	for(i = 0; i<len;i++){
		if(str[i] == c){
			break;
		}
	}
	return strcut(str,0,i);
}
char* strcut(char *str, int begin,int end){

	char *aux = str;
	int len = strlen(aux);
	if(end > 0){
		aux[end] ='\0';
	}
	if(begin < len){
		aux = &aux[begin];
	}

	return aux;
}