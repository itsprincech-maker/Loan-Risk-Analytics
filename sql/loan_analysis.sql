-- ============================================================
-- LOAN APPROVAL & RISK ANALYTICS
-- STEP 7: SQL BUSINESS ANALYSIS
-- ============================================================

-- ============================================================
-- 1. CREATE DATABASE
-- ============================================================

CREATE DATABASE loan_risk_analytics;

USE loan_risk_analytics;


-- ============================================================
-- 2. CREATE LOAN APPLICATIONS TABLE
-- ============================================================

CREATE TABLE loan_applications (

    Loan_ID VARCHAR(30),

    Gender VARCHAR(20),

    Married VARCHAR(20),

    Dependents VARCHAR(20),

    Education VARCHAR(30),

    Self_Employed VARCHAR(20),

    ApplicantIncome DECIMAL(12,2),

    CoapplicantIncome DECIMAL(12,2),

    LoanAmount DECIMAL(12,2),

    Loan_Amount_Term INT,

    Credit_History INT,

    Property_Area VARCHAR(30),

    Loan_Status VARCHAR(5)

);


-- ============================================================
-- 3. LOAD DATA
-- ============================================================

-- Update the file path according to your MySQL setup.

-- Example:
-- LOAD DATA LOCAL INFILE
-- 'C:/Users/Princ/OneDrive/Desktop/Loan-Risk-Analytics/data/loan_cleaned.csv'
-- INTO TABLE loan_applications
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;


-- ============================================================
-- 4. CHECK TOTAL APPLICATIONS
-- ============================================================

SELECT
    COUNT(*) AS total_applications
FROM loan_applications;


-- ============================================================
-- 5. APPROVED VS REJECTED APPLICATIONS
-- ============================================================

SELECT
    Loan_Status,
    COUNT(*) AS application_count
FROM loan_applications
GROUP BY Loan_Status;


-- ============================================================
-- 6. APPROVAL RATE
-- ============================================================

SELECT

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'N' THEN 1
            ELSE 0
        END
    ) AS rejected_applications,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications;


-- ============================================================
-- 7. APPROVAL RATE BY CREDIT HISTORY
-- ============================================================

SELECT

    Credit_History,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Credit_History

ORDER BY approval_rate DESC;


-- ============================================================
-- 8. APPROVAL RATE BY EDUCATION
-- ============================================================

SELECT

    Education,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Education

ORDER BY approval_rate DESC;


-- ============================================================
-- 9. APPROVAL RATE BY PROPERTY AREA
-- ============================================================

SELECT

    Property_Area,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Property_Area

ORDER BY approval_rate DESC;


-- ============================================================
-- 10. APPROVAL RATE BY SELF EMPLOYMENT
-- ============================================================

SELECT

    Self_Employed,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Self_Employed;


-- ============================================================
-- 11. AVERAGE APPLICANT INCOME
-- ============================================================

SELECT

    Loan_Status,

    ROUND(AVG(ApplicantIncome), 2)
        AS average_applicant_income

FROM loan_applications

GROUP BY Loan_Status;


-- ============================================================
-- 12. AVERAGE LOAN AMOUNT
-- ============================================================

SELECT

    Loan_Status,

    ROUND(AVG(LoanAmount), 2)
        AS average_loan_amount

FROM loan_applications

GROUP BY Loan_Status;


-- ============================================================
-- 13. HIGH LOAN AMOUNT APPLICATIONS
-- ============================================================

SELECT

    Loan_ID,

    ApplicantIncome,

    CoapplicantIncome,

    LoanAmount,

    Credit_History,

    Property_Area,

    Loan_Status

FROM loan_applications

WHERE LoanAmount >
(
    SELECT AVG(LoanAmount)
    FROM loan_applications
)

ORDER BY LoanAmount DESC;


-- ============================================================
-- 14. HIGH-RISK APPLICATIONS
-- ============================================================

SELECT

    Loan_ID,

    ApplicantIncome,

    CoapplicantIncome,

    LoanAmount,

    Credit_History,

    Education,

    Property_Area,

    Loan_Status

FROM loan_applications

WHERE Credit_History = 0

ORDER BY LoanAmount DESC;


-- ============================================================
-- 15. INCOME SEGMENT ANALYSIS
-- ============================================================

SELECT

    CASE

        WHEN ApplicantIncome < 3000
            THEN 'Low Income'

        WHEN ApplicantIncome BETWEEN 3000 AND 7000
            THEN 'Medium Income'

        ELSE 'High Income'

    END AS income_segment,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY income_segment

ORDER BY approval_rate DESC;


-- ============================================================
-- 16. DEPENDENTS ANALYSIS
-- ============================================================

SELECT

    Dependents,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Dependents

ORDER BY approval_rate DESC;


-- ============================================================
-- 17. GENDER ANALYSIS
-- ============================================================

SELECT

    Gender,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Gender;


-- ============================================================
-- 18. MARRIAGE STATUS ANALYSIS
-- ============================================================

SELECT

    Married,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY Married;


-- ============================================================
-- 19. LOAN BURDEN ANALYSIS
-- ============================================================

SELECT

    Loan_ID,

    ApplicantIncome,

    CoapplicantIncome,

    LoanAmount,

    ROUND(
        LoanAmount /
        NULLIF(
            ApplicantIncome + CoapplicantIncome,
            0
        ),
        2
    ) AS loan_income_ratio,

    Loan_Status

FROM loan_applications

ORDER BY loan_income_ratio DESC;


-- ============================================================
-- 20. TOP 10 HIGHEST LOAN BURDEN APPLICATIONS
-- ============================================================

SELECT

    Loan_ID,

    ApplicantIncome,

    CoapplicantIncome,

    LoanAmount,

    ROUND(
        LoanAmount /
        NULLIF(
            ApplicantIncome + CoapplicantIncome,
            0
        ),
        2
    ) AS loan_income_ratio,

    Credit_History,

    Loan_Status

FROM loan_applications

ORDER BY loan_income_ratio DESC

LIMIT 10;


-- ============================================================
-- 21. CREDIT HISTORY + EDUCATION ANALYSIS
-- ============================================================

SELECT

    Credit_History,

    Education,

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y' THEN 1
            ELSE 0
        END
    ) AS approved,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate

FROM loan_applications

GROUP BY
    Credit_History,
    Education

ORDER BY approval_rate DESC;


-- ============================================================
-- 22. EXECUTIVE BUSINESS SUMMARY
-- ============================================================

SELECT

    COUNT(*) AS total_applications,

    SUM(
        CASE
            WHEN Loan_Status = 'Y'
            THEN 1
            ELSE 0
        END
    ) AS approved_loans,

    SUM(
        CASE
            WHEN Loan_Status = 'N'
            THEN 1
            ELSE 0
        END
    ) AS rejected_loans,

    ROUND(
        AVG(ApplicantIncome),
        2
    ) AS avg_applicant_income,

    ROUND(
        AVG(LoanAmount),
        2
    ) AS avg_loan_amount,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Loan_Status = 'Y'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS overall_approval_rate

FROM loan_applications;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================