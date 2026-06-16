#include <check.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* Declare the function from nvidia-extract.c */
extern char *replace_string(const char *buffer, const char *search, const char *replacement);

START_TEST(test_replace_string_bounds_safety)
{
    /* Invariant: replace_string must not corrupt heap when replacement is longer than search */
    
    /* Test cases: exploit case (large replacement), boundary (empty strings), valid input */
    struct {
        const char *buffer;
        const char *search;
        const char *replacement;
    } cases[] = {
        /* Exploit case: replacement much longer than search, multiple occurrences */
        {"AAAA", "A", "XXXXXXXXXXXXXXXXXXXX"},
        /* Boundary: empty replacement */
        {"test string test", "test", ""},
        /* Valid normal case */
        {"hello world", "world", "universe"},
        /* Boundary: search not found */
        {"no match here", "xyz", "replacement"},
    };
    int num_cases = sizeof(cases) / sizeof(cases[0]);

    for (int i = 0; i < num_cases; i++) {
        char *result = replace_string(cases[i].buffer, cases[i].search, cases[i].replacement);
        
        /* Security invariant: result must be valid or NULL, never corrupted */
        if (result != NULL) {
            /* Result length must be calculable and string must be properly terminated */
            size_t len = strlen(result);
            ck_assert_msg(len < 10000, "Result length suspiciously large, possible corruption");
            
            /* If search was found, replacement should appear in result */
            if (strstr(cases[i].buffer, cases[i].search) != NULL && strlen(cases[i].replacement) > 0) {
                ck_assert_msg(strstr(result, cases[i].replacement) != NULL || 
                              strlen(cases[i].replacement) == 0,
                              "Replacement not found in result");
            }
            free(result);
        }
    }
}
END_TEST

Suite *security_suite(void)
{
    Suite *s;
    TCase *tc_core;

    s = suite_create("Security");
    tc_core = tcase_create("Core");

    tcase_add_test(tc_core, test_replace_string_bounds_safety);
    suite_add_tcase(s, tc_core);

    return s;
}

int main(void)
{
    int number_failed;
    Suite *s;
    SRunner *sr;

    s = security_suite();
    sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);

    return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}