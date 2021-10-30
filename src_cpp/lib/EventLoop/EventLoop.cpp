#include <vector>
#include <queue>

#include <EventLoop.hpp>


std::priority_queue<Job, std::vector<Job>, std::greater<Job>> jobs;


bool operator < (const Job& first, const Job& second) {
    return first.getExecutionTime() < second.getExecutionTime();
}

bool operator > (const Job& first, const Job& second) {
    return first.getExecutionTime() > second.getExecutionTime();
}

unsigned long Job::getExecutionTime() const {
    return executionTime;
}

std::function<void()> Job::getJob() const {
    return job;
}

Job::Job(unsigned long executionTime, std::function<void()> job) : executionTime(executionTime), job(job) {}

void addJob(unsigned long executionTime, std::function<void()> job) {
    jobs.push(Job(executionTime, job));
}

void executeJobs(unsigned long currentMillis) {
    while(jobs.size() > 0 && jobs.top().getExecutionTime() <= currentMillis) {
        jobs.top().getJob()();
        jobs.pop();
    }
}
