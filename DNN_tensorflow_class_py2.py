import matplotlib
matplotlib.use('TkAgg')
import tensorflow as tf
import numpy as np
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
#from mnist import load_mnist
import matplotlib.pyplot as plt
import os

class EarlyStopping():
    def __init__(self, patience=10, verbose=1):
        self._step = 0
        self._loss = float('inf')
        self.patience = patience
        self.verbose = verbose
    
    def validate(self, loss):
        if self._loss < loss:
            self._step += 1
            #print(self._step)
            if self._step > self.patience:
                if self.verbose:
                    print('********* Early Stopping **********')
                return True
        else:
            self._step = 0
            self._loss = loss

        return False


class DNN(object):
    def __init__(self, n_in, n_hiddens, n_out):
        ## initialize
        self.n_in = n_in
        self.n_hiddens = n_hiddens
        self.n_out = n_out
        self.weights = []
        self.biases = []
        self._x = None
        self._y = None
        self._t = None
        self._keep_prob = None
        self._sess = None
        self._history = {'accuracy':[], 'loss':[]}
        self._val_history = {'val_acc':[], 'val_loss':[]}

    def weight_variable(self,shape, name=None): ##FIXME TODO Initialize the weight value
        #initial = tf.truncated_normal(shape, stddev=0.01)  # truncated normal distribution
        #initial = tf.convert_to_tensor(np.random.uniform(low=-np.sqrt(1.0/shape[0]), high=np.sqrt(1.0/shape[0]), size=shape),np.float32) # uniform distribution
        #initial = tf.contrib.layers.xavier_initializer(uniform=False) #Glorot gaussian(False) or uniform(True) distribution
        initial = np.sqrt(2.0/shape[0]) * tf.truncated_normal(shape) # He's normal distribution For 'relu' activation
        #print(initial)
        return tf.Variable(initial, name=name)


    def bias_variable(self,shape, name=None):
        initial = tf.zeros(shape)
        return tf.Variable(initial, name=name)

    def batch_normalization(self, shape, x,nameb=None, nameg=None): 
        eps = 1e-8
        beta = tf.Variable(tf.zeros(shape), name=nameb)
        gamma = tf.Variable(tf.ones(shape), name=nameg)
        mean, var = tf.nn.moments(x, [0])
        #print((gamma * (x - mean)/tf.sqrt(var + eps) + beta).shape)
        return gamma * (x - mean)/tf.sqrt(var + eps) + beta


    def inference(self, x, keep_prob):
        #define a certain model
        ## input_layer - hidden_layer && hidden_layer - hidden_layer :: using for loop
        for i, n_hidden in enumerate(self.n_hiddens):
            if i == 0:
                Input = x    # input may cause error, since python2...
                input_dim = self.n_in
            else:
                Input = output
                input_dim = self.n_hiddens[i-1]
            self.weights.append(self.weight_variable([input_dim,n_hidden],name='W_{}'.format(i)))
            self.biases.append(self.bias_variable([n_hidden],'b_{}'.format(i)))

            u = tf.matmul(Input, self.weights[-1])      #FIXME Added for batch normalization
            h = self.batch_normalization([n_hidden],u, nameb='b_{}'.format(i), nameg='g_{}'.format(i))  #FIXME Added for batch normalization
            output = tf.nn.relu(h)                      #FIXME Added for batch normalization ## using relu  ## TODO 'activation function'
            #output = tf.nn.dropout(output, keep_prob)   #FIXME Added for batch normalization ## using relu  ## TODO '(un)comment'

            #h = tf.nn.relu(tf.matmul(Input, self.weights[-1]) + self.biases[-1])  ## using relu  ##FIXME wihtout batch_norm
            #output = tf.nn.dropout(h, keep_prob)
        
        ## hidden_layer - output_layer
        self.weights.append(self.weight_variable([self.n_hiddens[-1],self.n_out]))
        self.biases.append(self.bias_variable([self.n_out]))

        y = tf.nn.softmax(tf.matmul(output,self.weights[-1]) + self.biases[-1])   ## using softmax  ## FIXME
        return y

    def inference_regression(self, x, keep_prob): #FIXME #TODO
        #define a certain model
        ## input_layer - hidden_layer && hidden_layer - hidden_layer :: using for loop
        for i, n_hidden in enumerate(self.n_hiddens):
            if i == 0:
                Input = x    # input may cause error, since python2...
                input_dim = self.n_in
            else:
                Input = output
                input_dim = self.n_hiddens[i-1]
            self.weights.append(self.weight_variable([input_dim,n_hidden],name='W_{}'.format(i)))
            self.biases.append(self.bias_variable([n_hidden],'b_{}'.format(i)))

            u = tf.matmul(Input, self.weights[-1])      #FIXME Added for batch normalization
            h = self.batch_normalization([n_hidden],u, nameb='b_{}'.format(i), nameg='g_{}'.format(i))  #FIXME Added for batch normalization
            output = tf.nn.relu(h)                      #FIXME Added for batch normalization ## using relu  ## TODO 'activation function'
            #output = tf.nn.dropout(output, keep_prob)   #FIXME Added for batch normalization ## using relu  ## TODO '(un)comment'

            #h = tf.nn.relu(tf.matmul(Input, self.weights[-1]) + self.biases[-1])  ## using relu  ##FIXME wihtout batch_norm
            #output = tf.nn.dropout(h, keep_prob)

        ## hidden_layer - output_layer
        self.weights.append(self.weight_variable([self.n_hiddens[-1],self.n_out]))
        self.biases.append(self.bias_variable([self.n_out]))
        y = tf.matmul(output,self.weights[-1]) + self.biases[-1]   ## using ~~  ## FIXME
        return y
        


    def loss(self, y, t):
        #cross_entropy = tf.reduce_mean(-tf.reduce_sum(t*tf.log(y), reduction_indices=[1]))  #old one
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(t * tf.log(tf.clip_by_value(y,1e-10, 1.0)), reduction_indices=[1]))
        return cross_entropy

    def loss_regression(self, y, t):
        cross_entropy = tf.losses.mean_squared_error(t,y)
#        cross_entropy = tf.reduce_mean(-tf.reduce_sum(t * tf.log(tf.clip_by_value(y,1e-10, 1.0)), reduction_indices=[1]))
        return cross_entropy
#        pass


    def training(self, loss):  ## FIXME TODO select optimizer
        #optimizer = tf.train.GradientDescentOptimizer(0.01)
        #optimizer = tf.train.MomentumOptimizer(0.01, 0.9)  # Momentum(gamma=0.9)
        #optimizer = tf.train.MomentumOptimizer(0.01, 0.9, use_nesterov=True) # Nesterov Momentum
        #optimizer = tf.train.AdagradOptimizer(0.01) # Adagrad, not recommended
        #optimizer = tf.train.AdadeltaOptimizer(learning_rate=1.0, rho=0.95)
        #optimizer = tf.train.RMSPropOptimizer(0.001) # Similar with AdadeltaOptimizer
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001, beta1=0.9, beta2=0.999) ## recommended
        train_step = optimizer.minimize(loss)
        return train_step

    def accuracy(self, y, t):
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(t,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return accuracy

    '''
    def Data_normalization(self,X_DATA_in):
        X = X_DATA_in
        X = X / X.max()
        #print(len(X[0]))
        #for i in range(len(X[0])):
        #    print(X[0][i],end= ' ')
        X = X - X.mean(axis=1).reshape(len(X),1)
        return X
    '''

    def fit_classify(self, X_train, Y_train, X_validation, Y_validation, epochs=100, batch_size=100, p_keep=0.5, earlyStop=30, model_name='tensorflow_model',verbose=1):
        Model_NAME = "/" + model_name + "_EP{}.ckpt"
        #if(Data_normalize):
        #    X_train = self.Data_normalization(X_train)
        #    X_validation = self.Data_normalization(X_validation)
 
        MODEL_DIR = os.path.join(os.path.dirname(__file__),'tens_model_class')
        if os.path.exists(MODEL_DIR) is False:
            os.mkdir(MODEL_DIR)

        x = tf.placeholder(tf.float32, shape=[None,self.n_in])
        t = tf.placeholder(tf.float32, shape=[None,self.n_out])
        keep_prob = tf.placeholder(tf.float32)

        self._x = x
        self._t = t
        self._keep_prob = keep_prob

        y = self.inference(x,keep_prob)
        self._y = y 
        loss = self.loss(y,t)
        train_step = self.training(loss)
        accuracy = self.accuracy(y,t)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        sess = tf.Session()
        sess.run(init)

        self._sess = sess

        N_train = len(X_train)
        n_batches = N_train//batch_size

        early_stopping = EarlyStopping(patience=earlyStop, verbose=1)   #FIXME Early stopping factor
        one_third = 0; two_third = 0
        for epoch in range(epochs):
#            print("Epoch :",epoch+1, " :: ", (str(epoch+1)+"/"+str(epochs)),end='\t')
            print "Epoch :", epoch+1, " :: ", (str(epoch+1)+"/"+str(epochs)),"\t",
            X_, Y_ = shuffle(X_train, Y_train)

            for i in range(n_batches):
                start = i * batch_size
                end = start + batch_size
                sess.run(train_step, feed_dict={x:X_[start:end], t:Y_[start:end], keep_prob:p_keep})

            val_loss = round(loss.eval(session=sess, feed_dict={x:X_validation, t:Y_validation, keep_prob:1.0}),4)
            val_acc = round(accuracy.eval(session=sess, feed_dict={x:X_validation, t:Y_validation, keep_prob:1.0}),4)
            self._val_history['val_loss'].append(val_loss)
            self._val_history['val_acc'].append(val_acc)
            #print('val_loss =',val_loss, '\t', 'val_acc =',val_acc,end='\t')
            print 'val_loss =', val_loss, '\t', 'val_acc =', val_acc, '\t',

            loss_ = round(loss.eval(session=sess, feed_dict={x: X_train, t:Y_train, keep_prob:1.0}),4)
            accuracy_ = round(accuracy.eval(session=sess, feed_dict={x: X_train, t:Y_train, keep_prob:1.0}),4)
            self._history['loss'].append(loss_)
            self._history['accuracy'].append(accuracy_)

            if verbose:
                print 'train_loss =', loss_,'\t', 'train_accuracy =',accuracy_

            if((one_third==0) & (epochs//(epoch+1) == 3)): 
                one_third = 1
                model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
                print 'Model has been saved to:', model_path
            if((two_third==0) & (float(epoch+1)/float(epochs)>0.67)):
                two_third = 1
                model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
                print 'Model has been saved to:', model_path

            if early_stopping.validate(val_loss):
                break

        model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
        print 'Model has been saved to:', model_path
        return self._history


    def regression_accuracy(self, y, t):  #FIXME
        correct_prediction = tf.subtract(y, t)
        error = tf.sqrt(tf.square(correct_prediction))
        #correct_prediction = t - correct_prediction
        total_error = tf.reduce_mean(error)
        return total_error


    def fit_regression(self, X_train, Y_train, X_validation, Y_validation, epochs=100, batch_size=100, p_keep=0.5, earlyStop=30, model_name='tensorflow_model',verbose=1):
        Model_NAME = "/" + model_name + "_EP{}.ckpt"
        #if(Data_normalize):
        #    X_train = self.Data_normalization(X_train)
        #    X_validation = self.Data_normalization(X_validation)

        MODEL_DIR = os.path.join(os.path.dirname(__file__),'tens_model_reg')
        if os.path.exists(MODEL_DIR) is False:
            os.mkdir(MODEL_DIR)

        x = tf.placeholder(tf.float32, shape=[None,self.n_in])
        t = tf.placeholder(tf.float32, shape=[None,self.n_out])
        keep_prob = tf.placeholder(tf.float32)

        self._x = x
        self._t = t
        self._keep_prob = keep_prob

        y = self.inference_regression(x,keep_prob)
        self._y = y
        loss = self.loss_regression(y,t)
        train_step = self.training(loss)
        accuracy = self.regression_accuracy(y,t)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        sess = tf.Session()
        sess.run(init)

        self._sess = sess

        N_train = len(X_train)
        n_batches = N_train//batch_size

        early_stopping = EarlyStopping(patience=earlyStop, verbose=1)   #FIXME Early stopping factor
        one_third = 0; two_third = 0
        for epoch in range(epochs):
            #print("Epoch :",epoch+1, " :: ", (str(epoch+1)+"/"+str(epochs)),end='\t')
            print "Epoch :",epoch+1, " :: ", (str(epoch+1)+"/"+str(epochs)), '\t',
            X_, Y_ = shuffle(X_train, Y_train)

            for i in range(n_batches):
                start = i * batch_size
                end = start + batch_size
                sess.run(train_step, feed_dict={x:X_[start:end], t:Y_[start:end], keep_prob:p_keep})

            val_loss = round(loss.eval(session=sess, feed_dict={x:X_validation, t:Y_validation, keep_prob:1.0}),4)
            val_acc = round(accuracy.eval(session=sess, feed_dict={x:X_validation, t:Y_validation, keep_prob:1.0}),4)
            self._val_history['val_loss'].append(val_loss)
            self._val_history['val_acc'].append(val_acc)
            #print('val_loss =',val_loss, '\t', 'val_error =',val_acc,end='\t')
            print 'val_loss =',val_loss, '\t', 'val_error =',val_acc, '\t',
            #print('val_loss =',val_loss, '\t')

            #self_error = accuracy.eval(session=sess, feed_dict={x:X_validation, t:Y_validation, keep_prob:1.0})
            #print(self_error)  #FIXME
            #for i, tt in enumerate(self_error):
            #    print(tt,end='\t')

            loss_ = round(loss.eval(session=sess, feed_dict={x: X_train, t:Y_train, keep_prob:1.0}),4)
            accuracy_ = round(accuracy.eval(session=sess, feed_dict={x: X_train, t:Y_train, keep_prob:1.0}),4)
            self._history['loss'].append(loss_)
            self._history['accuracy'].append(accuracy_)

            if verbose:
                print 'train_loss =', loss_,'\t', 'train_error =',accuracy_
                #print ('train_loss =', loss_,'\t')

            if((one_third==0) & (epochs//(epoch+1) == 3)):
                one_third = 1
                model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
                print 'Model has been saved to:', model_path
            if((two_third==0) & (float(epoch+1)/float(epochs)>0.67)):
                two_third = 1
                model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
                print 'Model has been saved to:', model_path

            if early_stopping.validate(val_loss):
                break

        model_path = saver.save(sess, MODEL_DIR + Model_NAME.format(epoch+1))
        print 'Model has been saved to:', model_path
        return self._history


    
    def fit_classify_model_read(self, ModelName, keep_prob=0.5):
        x = tf.placeholder(tf.float32, shape=[None,self.n_in])
        t = tf.placeholder(tf.float32, shape=[None,self.n_out])
        keep_prob = tf.placeholder(tf.float32)

        self._x = x
        self._t = t
        self._keep_prob = keep_prob

        y = self.inference(x,keep_prob)
        self._y = y
        loss = self.loss(y,t)
        train_step = self.training(loss)
        accuracy = self.accuracy(y,t)
        saver = tf.train.Saver()
        sess = tf.Session()
        self._sess = sess
        saver.restore(sess, ModelName)

    '''
    def accuracy(self, y, t):
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(t,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return accuracy
    ''' 

    def Indicate_classified_LL_TTTL(self, X, Y):
#        prediction = tf.argmax(self._y,1)
        prediction = self._y 
        eval_pred = prediction.eval(session=self._sess, feed_dict={self._x: X, self._t: Y, self._keep_prob: 1.0})
        LL=0; TTTL=0
        for i in range(len(eval_pred)):
            if(eval_pred[i][0] > eval_pred[i][1]): 
                LL += 1
            else: 
                TTTL += 1
        print("LL :",LL)
        print("TTTL :", TTTL)
        return_tuple = (LL,TTTL,eval_pred)
        return return_tuple


    def evaluate(self, X_test, Y_test):
        accuracy = self.accuracy(self._y, self._t)
        return accuracy.eval(session=self._sess, feed_dict={self._x: X_test, self._t: Y_test, self._keep_prob: 1.0})
        #accuracy = self.accuracy(y,t)
        #accuracy_ = accuracy.eval(session=self._sess, feed_dict={self._x:X_test, self._t:Y_test, self._keep_prob:1.0}) 
        #return accuracy_
        #return self.accuracy.eval(session=self._sess, feed_dict={self._x:X_test, self._t:Y_test, self._keep_prob:1.0})

    def Plot_acc_loss(self,plot_name='tensorflow_test.pdf'):
        history_epochs = len(self._val_history['val_loss'])
        epochs = history_epochs
        fig = plt.figure()
        ax_acc = fig.add_subplot(111)
        ax_acc.plot(range(epochs), self._val_history['val_acc'], label='val_acc', color='blue')
        ax_acc.set_xlabel('Epoch')
        ax_acc.set_ylabel('validation accuracy', color='blue')
        ax_loss = ax_acc.twinx()
        ax_loss.plot(range(epochs), self._val_history['val_loss'], label='val_loss', color='red')        
        ax_loss.set_ylabel('validation loss-value', color='red')
        ax_loss_train = ax_acc.twinx()
        ax_loss_train.plot(range(epochs), self._history['loss'], label='train_loss', color='green')
        ax_acc.plot(np.nan, 'r', label="val_loss")
        ax_acc.plot(np.nan, 'g', label="train_loss")
        ax_acc.legend(loc=0)
        plt.xlabel('epochs')
        #plt.show()
        plt.savefig(plot_name)

    def Plot_error_loss(self,plot_name='tensorflow_test.pdf'):
        history_epochs = len(self._val_history['val_loss'])
        epochs = history_epochs
        fig = plt.figure()
        ax_acc = fig.add_subplot(111)
        ax_acc.plot(range(epochs), self._val_history['val_acc'], label='val_error', color='blue')
        ax_acc.set_xlabel('Epoch')
        ax_acc.set_ylabel('validation error', color='blue')
        ax_loss = ax_acc.twinx()
        ax_loss.plot(range(epochs), self._val_history['val_loss'], label='val_loss', color='red')
        ax_loss.set_ylabel('validation loss-value', color='red')
        ax_loss_train = ax_acc.twinx()
        ax_loss_train.plot(range(epochs), self._history['loss'], label='train_loss', color='green')
        ax_acc.plot(np.nan, 'r', label="val_loss")
        ax_acc.plot(np.nan, 'g', label="train_loss")
        ax_acc.legend(loc=0)
        plt.xlabel('epochs')
        #plt.show()
        plt.savefig(plot_name)




def main():
    model = DNN(n_in=784, n_hiddens=[200,200,200], n_out=10)
    epochs = 100  #FIXME
    earlyStop = 50 #epochs//5
    batch_size = 200
    model_name = "mnist_tensor"

    ##### prepare data
    N_train = 40000
    N_validation = 4000
    #(X_train,Y_train),(X_test,Y_test) = load_mnist(flatten=True, normalize=False, one_hot_label=True) 
    #X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, train_size=N_train)   #train_test_split
    ##print(X_train.shape);print(X_test.shape);print(Y_train.shape);print(Y_test.shape)
    #X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=N_validation)
    ##print(X_train.shape);print(X_validation.shape);print(Y_train.shape);print(Y_validation.shape)
    ######

    '''
    # 1. Loading existing model
    model.fit_classify_model_read(ModelName="/Users/leejunho/Desktop/git/python3Env/group_study/DNN_study/chapter04/tens_model/mnist_tensor_EP20.ckpt") # TODO for load in store Model
    accuracy = model.evaluate(X_test, Y_test)
    print('accuracy:', accuracy)
    '''

    
    ## 2. classification model
    model.fit_classify(X_train, Y_train, X_validation, Y_validation, epochs=epochs, batch_size=batch_size, p_keep=0.5, earlyStop=earlyStop, model_name = model_name)
    accuracy = model.evaluate(X_test, Y_test)
    print('accuracy:', accuracy)
    model.Plot_acc_loss(plot_name='mnist_tensorflow.pdf')
    
    '''
    # 3. regression model
    model.fit_regression(X_train, Y_train, X_validation, Y_validation, epochs=epochs, batch_size=batch_size, p_keep=0.5, earlyStop=earlyStop, model_name = model_name)
    model.Plot_error_loss(plot_name='mnist_tensorflow.pdf')
    '''


if __name__=="__main__":
    main()


