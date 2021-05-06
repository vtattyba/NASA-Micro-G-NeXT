%Test model for the effect of different nozzle parameters on 
%performance

AR = linspace(1,10,100);%area ratio of the nozzle
Wm = 70;%work done by the motor
n = 0.8;%efficiency of the motor/prop combo
vi = 0;%the velocity of the input fluid
%% Varying AR
ve = calcVe(AR,n,Wm,vi);

figure(1);
subplot(2,1,1);
grid on;
hold on;
plot(AR,ve);
xlabel('Nozzle Area Ratio');
ylabel('Exit Velocity(m/s)');

subplot(2,1,2);
mDot = calcMdot(ve);
plot(ve,mDot);
grid on;
xlabel('Exit Velocity(m/s)');
ylabel('Mass Flow Rate Required(kg/s)');
hold off;
%% Varying n
figure(2);
subplot(2,1,1);
AR = 2;
n = linspace(0,1,100);
ve = calcVe(AR,n,Wm,vi);
grid on;
hold on;
plot(n,ve);
xlabel('Propeller Efficiency');
ylabel('Exit Velocity(m/s)');

subplot(2,1,2);
mDot = calcMdot(ve);
plot(ve,mDot);
grid on;
xlabel('Exit Velocity(m/s)');
ylabel('Mass Flow Rate Required(kg/s)');
hold off;

%% Varying vi
n = 0.8;
vi = linspace(0,5.2,100);
ve = calcVe(AR,n,Wm,vi);

figure(3);
subplot(2,1,1);
grid on;
hold on;
plot(vi,ve);
xlabel('Input Velocity(m/s)');
ylabel('Exit Velocity(m/s)');
hold off;

subplot(2,1,2);
mDot = calcMdot(ve);
plot(ve,mDot);
grid on;
xlabel('Exit Velocity(m/s)');
ylabel('Mass Flow Rate Required(kg/s)');

%% Varying Wm
vi = 0;
Wm = linspace(0,100,100);
ve = calcVe(AR,n,Wm,vi);

figure(4);
subplot(2,1,1);
grid on;
hold on;
plot(Wm,ve);
xlabel('Motor Work(W)');
ylabel('Exit Velocity(m/s)');
hold off;

subplot(2,1,2);
mDot = calcMdot(ve);
plot(ve,mDot);
grid on;
xlabel('Exit Velocity(m/s)');
ylabel('Mass Flow Rate Required(kg/s)');

function ve = calcVe(AR,n,Wm,vi)
for i=1:100
    ve = AR*sqrt(2*(n.*Wm+vi.^2/2));
end
end

function mDot = calcMdot(ve);
Ft = 4.535;
mDot = Ft./ve;
end
