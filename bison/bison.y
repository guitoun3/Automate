%{
	#include <stdio.h>		
	#include <string.h>
%}

%union {
	char character;
	char* str;
}

%type <str> expr

%token <character> LETTER
%token EOL
%left '+'
%left LETTER CONCAT
%nonassoc '*'
%nonassoc '('

%%
input: /* empty */
	| input line
	;

line: expr EOL	{printf("\nExpression accepted : %s\n", $1);}
	| error EOL	{printf("\nExpression rejected\n");}
	;

expr: LETTER 					{char* s = malloc(sizeof(char) +2);
								sprintf(s, "\"%c\"", $1);
								$$ = s;}
	| expr expr %prec CONCAT	{char* s = malloc((strlen($1) + strlen($2)) * sizeof(char) +11);
								sprintf(s, "[\".\", [%s, %s]]", $1, $2);
								$$ = s;}
	| expr '+'  expr 			{char* s = malloc((strlen($1) + strlen($3)) * sizeof(char) +11);
								sprintf(s, "[\"+\", [%s, %s]]", $1, $3);
								$$ = s;}
	| '(' expr ')'				{char* s = malloc((strlen($2)) * sizeof(char) +2);
								sprintf(s, "[%s]", $2);
								$$ = s;}
	| expr '*'					{char* s = malloc(strlen($1) * sizeof(char) +7);
								sprintf(s, "[\"*\", %s]", $1);
								$$ = s;}
	;

%%

yyerror(char* msg){
	printf("%s\n", msg);
}

int main(int argc, char *argv[]){
	yyparse();

	return 0;
}