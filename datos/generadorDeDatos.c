#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <time.h>
#define TAM 256

char* strTruncByChar(char *str, char c);
char* strcut(char *str, int begin,int end);	

int main(int argc, char const *argv[])
{
	FILE* dataFile;
	FILE* lastData;
	FILE* dataGenFile = fopen("dataGen.csv", "w");
	fclose(dataGenFile);
	char buffer[TAM];
	
	while(1){
		
		dataFile = fopen("data.csv", "r");

		//abre el archivo de datos dataGen en append
		dataGenFile = fopen("dataGen.csv", "a");
		//lee la primera linea y no la guarda porque ya esta guardaa
		fgets(buffer, TAM, dataFile);
		fclose(dataGenFile);

		while(fgets(buffer, TAM, dataFile)){

			strcpy(buffer,strTruncByChar(buffer,'\n'));
			//abre el archivo de datos dataGen en append
			dataGenFile = fopen("dataGen.csv", "a");
			//abre el archivo lastData en modo write
			lastData = fopen("lastData.csv", "w");	
			printf("%s\n", buffer);
			fprintf(dataGenFile, "%s\n", buffer);
			fprintf(lastData, "%s\n", buffer);
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