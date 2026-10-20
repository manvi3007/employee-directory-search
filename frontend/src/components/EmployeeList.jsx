import EmployeeCard from "./EmployeeCard";

export default function EmployeeList({ employees }) {
  return (
    <div className="employee-list">
      {employees.map((employee) => (
        <EmployeeCard key={employee.id} employee={employee} />
      ))}
    </div>
  );
}
