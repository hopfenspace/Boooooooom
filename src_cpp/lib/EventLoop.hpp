#ifndef EVENT_LOOP_HPP_
#define EVENT_LOOP_HPP_

#include <functional>
#include <queue>

class Job {
    public:
        Job(unsigned long executionTime, std::function<void()> job);

        unsigned long getExecutionTime() const;
        std::function<void()> getJob() const;

        friend bool operator < (const Job& first, const Job& second);
        friend bool operator > (const Job& first, const Job& second);

    private:
        unsigned long executionTime;
        std::function<void()> job;
};

void addJob(unsigned long executionTime, std::function<void()>);
void executeJobs(unsigned long currentMillis);

#endif